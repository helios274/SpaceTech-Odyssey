from django.utils.text import slugify
from django.db import models
from cloudinary.models import CloudinaryField
from account.models import User
from .utils import capitalize_words


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.name = capitalize_words(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_image = CloudinaryField('image')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    description = models.TextField(max_length=400, blank=True, null=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'


class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes_dislikes')
    like = models.BooleanField()

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{"Like" if self.like else "Dislike"} by {self.user.username} on {self.post.title}'


class Bookmark(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'Bookmark by {self.user.username} on {self.post.title}'
