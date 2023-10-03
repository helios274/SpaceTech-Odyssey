from django.urls import path
from . import views
urlpatterns = [
    path('auth/register', views.RegisterView.as_view(), name='register'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:id>', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update',
         views.UpdateProfileView.as_view(), name='update-profile')
]
