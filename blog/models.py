from django.db import models
from account.models import CustomUser
from django.utils.timezone import now
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BlogPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    tags = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(default=now)
    date_updated = models.DateTimeField(default=now)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']
