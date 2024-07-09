from django.contrib import admin
from .models import Tag, Post


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date_created')


admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
