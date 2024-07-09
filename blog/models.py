from django.utils.text import slugify
from django.db import models
from account.models import User
from django.utils.timezone import now
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
    thumbnail = models.ImageField(upload_to='blog/thumbnails/')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=400, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(default=now)
    date_updated = models.DateTimeField(default=now)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']


class Section(models.Model):
    post = models.ForeignKey(
        Post, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)


class ContentBlock(models.Model):
    section = models.ForeignKey(
        Section, related_name='%(class)ss', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TextBlock(ContentBlock):
    text = models.TextField()


class ImageBlock(ContentBlock):
    image = models.ImageField(upload_to='blog/images/')
    caption = models.CharField(max_length=255, blank=True, null=True)


class ListBlock(ContentBlock):
    LIST_TYPES = [
        ('b', 'Bullets'),
        ('1', 'Numbers'),
        ('A', 'Uppercase Letters'),
        ('a', 'Lowercase Letters'),
        ('I', 'Uppercase Roman numbers'),
        ('i', 'Lowercase Roman numbers'),
    ]

    items = models.TextField(help_text="Enter each item on a new line.")
    type = models.CharField(max_length=1, choices=LIST_TYPES, default='b')

    def get_items(self):
        return self.items.split('\n')
