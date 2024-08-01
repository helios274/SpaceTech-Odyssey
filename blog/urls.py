from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.AllPostsView.as_view(), name='all-posts'),
    path('posts/tag/<slug:slug>', views.PostsByTagView.as_view(), name='tag'),
    path('posts/create-post', views.CreatePostView.as_view(), name='create_post'),
    path('posts/search', views.SearchPostsView.as_view(), name='search-post'),
    path('posts/create-post/upload/post_cover',
         views.upload_image, name='upload_image'),
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/update', views.update_post, name='update_post'),
    path('posts/<slug:slug>/delete', views.delete_post, name='delete_post'),
    path('posts/<slug:slug>/like/', views.like_post, name='like_post'),
    path('posts/<slug:slug>/dislike/', views.dislike_post, name='dislike_post'),
    path('posts/<slug:slug>/bookmark/',
         views.bookmark_post, name='bookmark_post'),
    path('posts/<slug:slug>/status/',
         views.get_post_status, name='post_status'),
    path('posts/tags/search-tags',
         csrf_exempt(views.search_tags), name='search-tags'),
    path('posts/tags/add-tag', views.add_tag, name='add-tag'),

]
