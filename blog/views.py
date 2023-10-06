from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect("all-posts")
    posts = BlogPost.objects.all()[:2]
    return render(request, 'blog/index.html', {"posts": posts})


class AllPostsView(View):
    def get(self, request):
        posts = BlogPost.objects.all()
        paginator = Paginator(posts, 8)
        page_number = request.GET.get("page")
        page_object = Paginator.get_page(paginator, page_number)
        context = {
            "page_object": page_object,
            "posts_count": paginator.count
        }
        return render(request, 'blog/posts.html', context)


class PostDetailsView(DetailView):
    template_name = 'blog/post-details.html'
    model = BlogPost
    context_object_name = 'post'


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login'
    model = BlogPost
    form_class = PostForm
    template_name = 'blog/create-post.html'
    success_url = '/posts'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title[:50])
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login'
    model = BlogPost
    form_class = PostForm
    template_name = 'blog/update-post.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title[:50])
        form.instance.date_updated = now()
        messages.success(self.request, 'Post updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating the post.')
        return super().form_invalid(form)

    def get_success_url(self):
        success_url = reverse_lazy(
            'post-details', kwargs={'slug': self.object.slug})
        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the post object based on the view's model and URL parameters (pk or slug)
        post = get_object_or_404(BlogPost, slug=self.kwargs['slug'])
        context['post'] = post
        return context


@login_required
def delete_post(request, slug):
    post = BlogPost.objects.get(slug=slug)
    post.delete()
    messages.success(request, "Post deleted successfully")
    return redirect('profile', id=request.user.id)


class PostsByTagView(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug=slug)
        posts = BlogPost.objects.filter(tags=tag)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get("page")
        page_object = Paginator.get_page(paginator, page_number)
        context = {
            "tag": tag,
            "page_object": page_object,
            "posts_count": paginator.count
        }
        return render(request, 'blog/posts-by-tag.html', context)


class SearchPostsView(View):
    def post(self, request):
        search_str = request.POST['search_field']
        posts = (
            BlogPost.objects.filter(title__icontains=search_str)
            | BlogPost.objects.filter(tags__name__icontains=search_str)
        ).distinct()
        paginator = Paginator(posts, 8)
        page_number = request.GET.get("page")
        page_object = Paginator.get_page(paginator, page_number)
        context = {
            "page_object": page_object,
            "search_str": search_str,
            "posts_count": paginator.count
        }
        return render(request, 'blog/search-results.html', context)
