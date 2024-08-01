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
import mistletoe
import uuid
import cloudinary

from .models import Post, Tag, LikeDislike, Bookmark
from .forms import PostForm


def index(request):
    if request.user.is_authenticated:
        return redirect("all-posts")
    posts = Post.objects.all()[:3]
    return render(request, 'blog/index.html', {"posts": posts})


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'

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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']

        # Convert Markdown content to HTML
        post.content_html = mistletoe.markdown(post.content)

        # Fetch counts of likes, dislikes, and bookmarks
        likes_count = LikeDislike.objects.filter(post=post, like=True).count()
        dislikes_count = LikeDislike.objects.filter(
            post=post, like=False).count()
        bookmarks_count = Bookmark.objects.filter(post=post).count()

        # Add counts to the context
        context['likes_count'] = likes_count
        context['dislikes_count'] = dislikes_count
        context['bookmarks_count'] = bookmarks_count

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
            post = form.save()
            tags_string = request.POST.get('tags')
            if tags_string:
                tags = tags_string.split(',')
                post.tags.clear()  # Clear existing tags
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                    post.tags.add(tag)
            messages.success(request, "Post updated successfully")
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, "Invalid form data")

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/update_post.html', {"form": form})


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
        return render(request, 'blog/posts.html', context)


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
        return render(request, 'blog/posts.html', context)


class SearchPostsView(View):
    def post(self, request):
        search_str = request.POST['search_field']
        posts = (
            Post.objects.filter(title__icontains=search_str)
            | Post.objects.filter(tags__name__icontains=search_str)
            | Post.objects.filter(description__icontains=search_str)
        ).distinct()
        paginator = Paginator(posts, 8)
        page_number = request.GET.get("page")
        page_object = Paginator.get_page(paginator, page_number)
        context = {
            "page_object": page_object,
            "search_str": search_str,
            "posts_count": paginator.count
        }
        return render(request, 'blog/posts.html', context)
