from django.shortcuts import render, redirect
from .forms import LoginFrom, RegisterForm, ProfileEditForm, UserEditForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Posts

# Create your views here.
@login_required
def index(request):
    current_user = request.user
    user_posts = Posts.objects.filter(user=current_user)
    for post in user_posts:
        post.is_liked = current_user in post.liked_by.all()
    return render(request, 'users/index.html', {'posts': user_posts})

def login_view(request):
    form = LoginFrom()
    if request.method == 'POST':
        form = LoginFrom(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect('users:home')
            else:
                return HttpResponse("Invalid")
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'users/register_done.html')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponse("Profile updated successfully")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'users/edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'users/profile.html', {
        'user': request.user,
        'profile': profile,
    })