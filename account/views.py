from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages, auth
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import User
from blog.models import Post


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already registered")
            return redirect('/')
        form = RegisterForm()
        return render(request, 'account/register.html', {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(
                    request, "Email is already registered. Please Login")
                return render(request, 'account/register.html', {"form": form})
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                bio=form.cleaned_data['bio'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                password=form.cleaned_data['password'],
            )
            user.save()
            messages.success(request, "Account has been created.")
            return redirect('login')
        return render(request, 'account/register.html', {"form": form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in")
            return redirect('/')
        form = LoginForm()
        return render(request, 'account/login.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                if user.check_password(form.cleaned_data['password']):
                    auth.login(request, user)
                    messages.success(request, "Logged in successfully")
                    return redirect('all-posts')
                else:
                    messages.error(request, "Incorrect password")
                    return render(request, 'account/login.html', {"form": form})
            except:
                messages.error(request, "Invalid Credentials")
        return render(request, 'account/login.html', {"form": form})


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('/')


class ProfileView(View):
    def get(self, request, id):
        user = User.objects.get(id=id)
        posts = Post.objects.filter(author=user)
        paginator = Paginator(posts, 8)
        page_number = request.GET.get("page")
        page_object = Paginator.get_page(paginator, page_number)
        context = {"user_profile": user, "page_object": page_object,
                   "posts_count": paginator.count}
        return render(request, 'account/profile.html', context)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login'
    model = User
    form_class = ProfileUpdateForm
    template_name = 'account/update-profile.html'

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse_lazy('profile', args=[
                                   self.request.user.id])
        return success_url
