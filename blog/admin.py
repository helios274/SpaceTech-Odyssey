from django.contrib import admin
from .models import Tag, BlogPost


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date_created')


admin.site.register(Tag, TagAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
