from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.AllPostsView.as_view(), name='all-posts'),
    path('posts/tag/<slug:slug>', views.PostsByTagView.as_view(), name='tag'),
    path('posts/create-post', views.create_post, name='create-post'),
    path('posts/tags/search-tags',
         csrf_exempt(views.search_tags), name='search-tags'),
    path('posts/tags/add-tag', views.add_tag, name='add-tag'),
    path('posts/search', views.SearchPostsView.as_view(), name='search-post'),
    path('posts/<slug:slug>', views.post_details, name='post-details'),
    path('posts/<slug:slug>/update',
         views.UpdatePostView.as_view(), name='update-post'),
    path('posts/<slug:slug>/delete',
         views.delete_post, name='delete-post'),
]
