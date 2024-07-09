from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Tag, Section, TextBlock, ImageBlock, ListBlock
from .forms import (
    PostForm,
    CreateSectionFormset,
    CreateTextBlockFormset,
    CreateImageBlockFormset,
    CreateListBlockFormset,
)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from pprint import pprint


@login_required
def create_post(request):

    if request.method == 'POST':

        pprint(dict(request.POST))
        pprint(request.FILES)

        post_form = PostForm(request.POST, request.FILES)
        section_formset = CreateSectionFormset(
            request.POST, prefix='sections'
        )
        text_block_formset = CreateTextBlockFormset(
            request.POST, prefix='text_blocks'
        )
        image_block_formset = CreateImageBlockFormset(
            request.POST, request.FILES, prefix='image_blocks'
        )
        list_block_formset = CreateListBlockFormset(
            request.POST, prefix='list_blocks'
        )

        if (post_form.is_valid() and
            section_formset.is_valid() and
            text_block_formset.is_valid() and
            image_block_formset.is_valid() and
                list_block_formset.is_valid()):

            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            # post_form.save_m2m()

            section_formset_data = section_formset.cleaned_data
            sections = section_formset.save(commit=False)

            for i, section in enumerate(sections):

                section.post = post
                section.save()

                text_block_formset_data = text_block_formset.cleaned_data
                text_blocks = text_block_formset.save(commit=False)

                for j, text_block in enumerate(text_blocks):
                    if text_block_formset_data[j]['local_section_id'] == section_formset_data[i]['local_id']:
                        text_block.section = section
                        text_block.save()

                image_block_formset_data = image_block_formset.cleaned_data
                image_blocks = image_block_formset.save(commit=False)

                for j, image_block in enumerate(image_blocks):
                    if image_block_formset_data[j]['local_section_id'] == section_formset_data[i]['local_id']:
                        image_block.section = section
                        image_block.save()

                list_block_formset_data = list_block_formset.cleaned_data
                list_blocks = list_block_formset.save(commit=False)

                for j, list_block in enumerate(list_blocks):
                    if list_block_formset_data[j]['local_section_id'] == section_formset_data[i]['local_id']:
                        list_block.section = section
                        list_block.save()

            tags_string = request.POST.getlist('tags')
            tags = tags_string[0].split(',')
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            return redirect('create-post')

        else:
            messages.error(request, 'Form error')
            pprint(section_formset.errors)
            pprint(text_block_formset.errors)
            pprint(image_block_formset.errors)
            pprint(list_block_formset.errors)

    else:
        post_form = PostForm()
        section_formset = CreateSectionFormset(prefix='sections')
        text_block_formset = CreateTextBlockFormset(prefix='text_blocks')
        image_block_formset = CreateImageBlockFormset(prefix='image_blocks')
        list_block_formset = CreateListBlockFormset(prefix='list_blocks')

    context = {
        'post_form': post_form,
        'section_formset': section_formset,
        'text_block_formset': text_block_formset,
        'image_block_formset': image_block_formset,
        'list_block_formset': list_block_formset,
    }

    return render(request, 'blog/create-post.html', context)


def search_tags(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        tags = Tag.objects.filter(name__icontains=query).values('id', 'name')
        return JsonResponse(list(tags), safe=False)


def add_tag(request):
    pprint(request.headers)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        tag, created = Tag.objects.get_or_create(name=name)
        return JsonResponse({'id': tag.id, 'name': tag.name})


def index(request):
    if request.user.is_authenticated:
        return redirect("all-posts")
    posts = Post.objects.all()[:2]
    return render(request, 'blog/index.html', {"posts": posts})


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


def post_details(request, slug):
    if request.method == 'GET':
        post = Post.objects.get(slug=slug)
        sections = Section.objects.filter(post_id=post.id)
        text_blocks = []
        image_blocks = []
        list_blocks = []
        for section in sections:
            text_blocks += TextBlock.objects.filter(section_id=section.id)
            image_blocks += ImageBlock.objects.filter(section_id=section.id)
            list_blocks += ListBlock.objects.filter(section_id=section.id)

        context = {
            'post': post,
            'sections': sections,
            'text_blocks': text_blocks,
            'image_blocks': image_blocks,
            'list_blocks': list_blocks,
        }
        return render(request, 'blog/post-details.html', context)


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login'
    model = Post
    form_class = PostForm
    template_name = 'blog/create-post.html'
    success_url = '/posts'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title[:50])
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login'
    model = Post
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
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        context['post'] = post
        return context


@login_required
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    messages.success(request, "Post deleted successfully")
    return redirect('profile', id=request.user.id)


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
        return render(request, 'blog/posts-by-tag.html', context)


class SearchPostsView(View):
    def post(self, request):
        search_str = request.POST['search_field']
        posts = (
            Post.objects.filter(title__icontains=search_str)
            | Post.objects.filter(tags__name__icontains=search_str)
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
