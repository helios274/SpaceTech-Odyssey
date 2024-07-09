from typing import Any
from django import forms
from .models import Post, Section, TextBlock, ImageBlock, ListBlock
from .utils import generate_slug


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['thumbnail', 'title', 'description']

    def save(self, commit: bool = True) -> Any:
        post = super().save(commit=False)
        if not post.slug:
            post.slug = generate_slug(post.title)
        if commit:
            post.save()
        return post


class SectionForm(forms.ModelForm):
    local_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Section
        fields = ['title', 'subtitle', 'local_id']


class TextBlockForm(forms.ModelForm):
    local_section_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = TextBlock
        fields = ['text', 'local_section_id']


class ImageBlockForm(forms.ModelForm):
    local_section_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = ImageBlock
        fields = ['image', 'caption']


class ListBlockForm(forms.ModelForm):
    local_section_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = ListBlock
        fields = ['items', 'type', 'local_section_id']


CreateSectionFormset = forms.models.inlineformset_factory(
    Post, Section, SectionForm, extra=1, can_delete=False, max_num=20
)

CreateTextBlockFormset = forms.models.inlineformset_factory(
    Section, TextBlock, TextBlockForm, extra=1, can_delete=False, max_num=100
)

CreateImageBlockFormset = forms.models.inlineformset_factory(
    Section, ImageBlock, ImageBlockForm, extra=0, can_delete=False, max_num=10
)

CreateListBlockFormset = forms.models.inlineformset_factory(
    Section, ListBlock, ListBlockForm, extra=0, can_delete=False, max_num=50
)


UpdateSectionFormset = forms.models.inlineformset_factory(
    Post, Section, SectionForm, extra=0, can_delete=True
)
