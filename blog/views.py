from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count, Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta
import mistletoe
import uuid
import cloudinary
import datetime
from .models import Post, Tag, LikeDislike, Bookmark, Comment
from .forms import PostForm, CommentForm


@cache_page(60 * 10)
def index(request):
    recent_posts = Post.objects.all()[:3]

    cached_top_liked_posts = cache.get("top_liked_posts")
    if cached_top_liked_posts is None:
        top_liked_posts = Post.objects.annotate(
            total_likes=Count('likes_dislikes', filter=Q(
                likes_dislikes__like=True))
        ).order_by('-total_likes')[:5]
        cache.set("top_liked_posts", top_liked_posts, 60 * 60)
    else:
        top_liked_posts = cached_top_liked_posts

    cached_most_commented_posts = cache.get("most_commented_posts")
    if cached_most_commented_posts is None:
        most_commented_posts = Post.objects.annotate(
            total_comments=Count('comments')
        ).order_by('-total_comments')[:3]
        cache.set("most_commented_posts", most_commented_posts, 60 * 60)
    else:
        most_commented_posts = cached_most_commented_posts

    trending_posts = Post.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).annotate(
        total_activity=Count('likes_dislikes', filter=Q(
            likes_dislikes__like=True)) + Count('comments')
    ).order_by('-total_activity')[:3]

    context = {
        "recent_posts": recent_posts,
        "top_liked_posts": top_liked_posts,
        "most_commented_posts": most_commented_posts,
        "trending_posts": trending_posts,
    }

    return render(request, 'pages/blog/index.html', context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'pages/blog/create_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()
        tags_string = self.request.POST.get('tags')
        if tags_string:
            tags = tags_string.split(',')
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                post.tags.add(tag)
        return redirect('post_detail', slug=post.slug)


def upload_image(request):
    if request.method == 'POST':
        try:

            image_file = request.FILES['image']

            unique_filename = str(uuid.uuid4())

            # Upload image with additional options
            result = cloudinary.uploader.upload(
                image_file,
                # Set the public ID (filename in Cloudinary)
                public_id=unique_filename,
                # Upload to a specific Cloudinary folder (optional)
                folder=f"{settings.CLOUDINARY_ROOT_FOLDER}/post_images",
                # upload_preset=upload_preset,
                allowed_formats=["png", "jpg", "jpeg",
                                 "svg", "jfif", "ico", "webp"],
                overwrite=True,  # Ensures any existing file with the same public_id is overwritten
                resource_type="image"
            )
            return JsonResponse({'success': True, 'url': result['secure_url']})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests allowed'})


@method_decorator(cache_page(60 * 15), name='dispatch')
class PostDetailView(DetailView):
    model = Post
    template_name = 'pages/blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']

        # Convert Markdown content to HTML
        post.content_html = mistletoe.markdown(post.content)

        # Fetch counts of likes, dislikes, and bookmarks
        if self.request.user == post.author:
            likes_count = LikeDislike.objects.filter(
                post=post, like=True).count()
            dislikes_count = LikeDislike.objects.filter(
                post=post, like=False).count()
            bookmarks_count = Bookmark.objects.filter(post=post).count()

            # Add counts to the context
            context['likes_count'] = likes_count
            context['dislikes_count'] = dislikes_count
            context['bookmarks_count'] = bookmarks_count

        context['comment_form'] = CommentForm()

        return context


def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not post:
        messages.error(request, 'Post not found')
        return redirect('all-posts')
    if post.author_id != request.user.id:
        messages.error(
            request, "You do not have permission to update this post")
        return redirect("index")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = datetime.datetime.now()
            post.save()
            tags_string = request.POST.get('tags')
            if tags_string:
                tags = tags_string.split(',')
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                    post.tags.add(tag)
            messages.success(request, "Post updated successfully")
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, "Invalid form data")

    else:
        form = PostForm(instance=post)

    return render(request, 'pages/blog/update_post.html', {"form": form})


def get_post_status(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not request.user.is_authenticated:
        return JsonResponse({
            'liked': False,
            'disliked': False,
            'bookmarked': False
        })
    try:
        like_dislike = LikeDislike.objects.get(user=request.user, post=post)
        liked = like_dislike.like
        disliked = not like_dislike.like
    except LikeDislike.DoesNotExist:
        liked = False
        disliked = False

    try:
        bookmark = Bookmark.objects.get(user=request.user, post=post)
        bookmarked = True
    except Bookmark.DoesNotExist:
        bookmarked = False

    return JsonResponse({
        'liked': liked,
        'disliked': disliked,
        'bookmarked': bookmarked
    })


@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    try:
        like_dislike = LikeDislike.objects.get(user=request.user, post=post)
        if like_dislike.like:
            like_dislike.delete()
            status = 'removed'
        else:
            like_dislike.like = True
            like_dislike.save()
            status = 'liked'
    except LikeDislike.DoesNotExist:
        LikeDislike.objects.create(user=request.user, post=post, like=True)
        status = 'liked'
    return JsonResponse({'status': status})


@login_required
def dislike_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    try:
        like_dislike = LikeDislike.objects.get(user=request.user, post=post)
        if not like_dislike.like:
            like_dislike.delete()
            status = 'removed'
        else:
            like_dislike.like = False
            like_dislike.save()
            status = 'disliked'
    except LikeDislike.DoesNotExist:
        LikeDislike.objects.create(user=request.user, post=post, like=False)
        status = 'disliked'
    return JsonResponse({'status': status})


@login_required
def bookmark_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user, post=post)
    if not created:
        bookmark.delete()
        status = 'removed'
    else:
        status = 'bookmarked'
    return JsonResponse({'status': status})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not post:
        messages.error(request, 'Post not found')
        return redirect('all-posts')
    if post.author_id != request.user.id:
        messages.error(
            request, "You do not have permission to delete this post")
        return redirect("index")
    post.delete()
    messages.success(request, "Post deleted successfully")
    return redirect('profile', id=request.user.id)


@login_required
def search_tags(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        tags = Tag.objects.filter(name__icontains=query).values('id', 'name')
        return JsonResponse(list(tags), safe=False)


@login_required
def add_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        tag, created = Tag.objects.get_or_create(name=name)
        return JsonResponse({'id': tag.id, 'name': tag.name})


class AllPostsView(View):
    def get(self, request):
        posts = Post.objects.all()
        paginator = Paginator(posts, 8)
        page_number = request.GET.get("page")
        page_object = Paginator.get_page(paginator, page_number)
        context = {
            "page_object": page_object,
            "posts_count": paginator.count
        }
        return render(request, 'pages/blog/posts.html', context)


class PostsByTagView(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        posts = Post.objects.filter(tags=tag)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get("page")
        page_object = Paginator.get_page(paginator, page_number)
        context = {
            "tag": tag,
            "page_object": page_object,
            "posts_count": paginator.count
        }
        return render(request, 'pages/blog/posts.html', context)


class SearchPostsView(View):
    def post(self, request):
        search_str = request.POST['search_field']
        cache_key = f'search_{search_str}_page_{request.GET.get("page", 1)}'
        cached_posts = cache.get(cache_key)

        if cached_posts is None:
            posts = (
                Post.objects.filter(title__icontains=search_str)
                | Post.objects.filter(tags__name__icontains=search_str)
                | Post.objects.filter(description__icontains=search_str)
            ).distinct()
            paginator = Paginator(posts, 8)
            page_number = request.GET.get("page")
            page_object = Paginator.get_page(paginator, page_number)
            cache.set(cache_key, page_object, 60 * 15)  # Cache for 15 minutes
        else:
            page_object = cached_posts

        context = {
            "page_object": page_object,
            "search_str": search_str,
            "posts_count": paginator.count if cached_posts is None else len(page_object.object_list)
        }
        return render(request, 'pages/blog/posts.html', context)


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return JsonResponse({
                'id': comment.id,
                'user': comment.user.get_full_name(),
                'user_id': comment.user.id,
                'user_profile_photo': comment.user.profile_photo.url if comment.user.profile_photo else None,
                'content': comment.content,
                'created_at': comment.created_at.strftime("%B %d, %Y, %I:%M %p"),
                'parent': comment.parent.id if comment.parent else None,
            })
    return JsonResponse({'error': 'Invalid data'}, status=400)


def load_comments(request, post_id):
    offset = int(request.GET.get('offset') or 0)
    limit = int(request.GET.get('limit') or 5)
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None).order_by(
        '-created_at')[offset:offset + limit]
    comment_list = []
    for comment in comments:
        comment_list.append({
            'id': comment.id,
            'user': comment.user.get_full_name(),
            'user_id': comment.user.id,
            'user_profile_photo': comment.user.profile_photo.url if comment.user.profile_photo else None,
            'content': comment.content,
            'created_at': comment.created_at.strftime("%B %d, %Y, %I:%M %p"),
            'replies_count': comment.replies.count(),
            'parent': comment.parent.id if comment.parent else None,
        })
    return JsonResponse(comment_list, safe=False)


def load_replies(request, comment_id):
    offset = int(request.GET.get('offset') or 0)
    limit = int(request.GET.get('limit') or 5)
    comment = get_object_or_404(Comment, id=comment_id)
    replies = comment.replies.order_by('-created_at')[offset:offset + limit]
    reply_list = []
    for reply in replies:
        reply_list.append({
            'id': reply.id,
            'user': reply.user.get_full_name(),
            'user_id': reply.user.id,
            'user_profile_photo': reply.user.profile_photo.url if reply.user.profile_photo else None,
            'content': reply.content,
            'created_at': reply.created_at.strftime("%B %d, %Y, %I:%M %p"),
            'parent': reply.parent.id if reply.parent else None,
        })
    return JsonResponse(reply_list, safe=False)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if request.user == comment.user:
            content = request.POST.get('content')
            if content:
                comment.content = content
                comment.save()
                return JsonResponse({'content': comment.content})
    return JsonResponse({'error': 'Invalid data or unauthorized'}, status=400)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if request.user == comment.user or request.user == comment.post.user:
            comment.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid data or unauthorized'}, status=400)
