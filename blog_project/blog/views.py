from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

def is_author_or_superuser(user):
    """Check if user is the blog author or superuser"""
    return user.is_superuser or (user.is_authenticated and user.groups.filter(name='Blog Authors').exists())

def post_list(request):
    posts = BlogPost.objects.filter(published=True)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, published=True)
    comments = post.comments.filter(approved=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

@user_passes_test(is_author_or_superuser)
def post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create New Post'})

@user_passes_test(is_author_or_superuser)
def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Only allow editing if user is superuser or post author
    if not (request.user.is_superuser or post.author == request.user):
        messages.error(request, 'You can only edit your own posts.')
        return redirect('blog:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

@user_passes_test(is_author_or_superuser)
def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Only allow deletion if user is superuser or post author
    if not (request.user.is_superuser or post.author == request.user):
        messages.error(request, 'You can only delete your own posts.')
        return redirect('blog:post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
