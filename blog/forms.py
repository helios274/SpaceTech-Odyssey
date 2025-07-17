from typing import Any
from django import forms
from django.conf import settings
from .models import Post, Comment
from .utils import generate_slug
from cloudinary.forms import CloudinaryFileField


class PostForm(forms.ModelForm):
    cover_image = CloudinaryFileField(
        options={
            'folder': f'{settings.CLOUDINARY_ROOT_FOLDER}/post_covers',
            'transformation': [{'width': 800, 'height': 600, 'crop': 'limit'}],
        })
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, }),
        max_length=300,
        help_text="Max number of 300 characters"
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, }),
    )

    class Meta:
        model = Post
        fields = ['cover_image', 'title', 'description', 'content']

    def save(self, commit: bool = True) -> Any:
        post = super().save(commit=False)
        if not post.slug:
            post.slug = generate_slug(post.title)
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'}),
            'parent': forms.HiddenInput(),
        }
