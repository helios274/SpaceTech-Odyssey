from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.AllPostsView.as_view(), name='all-posts'),
    path('posts/tag/<slug:slug>', views.PostsByTagView.as_view(), name='tag'),
    path('posts/create-post', views.CreatePostView.as_view(), name='create-post'),
    path('posts/search', views.SearchPostsView.as_view(), name='search-post'),
    path('posts/<slug:slug>', views.PostDetailsView.as_view(), name='post-details'),
    path('posts/<slug:slug>/update',
         views.UpdatePostView.as_view(), name='update-post'),
    path('posts/<slug:slug>/delete',
         views.delete_post, name='delete-post'),
]
