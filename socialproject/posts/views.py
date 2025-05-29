from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Posts
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('users:home')
    else:
        form = PostForm()

    return render(request, 'posts/create.html', {'form': form})

def all_posts(request):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        new_comment = form.save(commit=False)
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Posts, id=post_id)
        new_comment.post = post
        new_comment.posted_by = request.user
        new_comment.save()
    else:
        form = CommentForm()


    posts = Posts.objects.select_related('user').prefetch_related('comments', 'liked_by').order_by('-date')
    for post in posts:
        post.is_liked = request.user in post.liked_by.all()

    return render(request, 'posts/all_posts.html', {'posts': posts, 'form': form})

def like_post(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = Posts.objects.get(id=post_id)
        user = request.user

        if user in post.liked_by.all():
            post.liked_by.remove(user)
            liked = False
        else:
            post.liked_by.add(user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': post.liked_by.count()
        })
    