from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.contrib import messages
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import AddPostForm, EditPostForm


def all_post(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_post.html', {'posts': posts})


def post_detail(request, post_id, slug):
    post = get_object_or_404(Post, pk=post_id, slug__exact=slug)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def add_post(request, user_id):
    if request.user.id == user_id:
        if request.method == 'POST':
            form = AddPostForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.slug = slugify(form.cleaned_data['body'[:30]])
                new_form.save()
                messages.success(request, 'Add post successfully')
                return redirect('account:user_dashboard', user_id)
        else:
            form = AddPostForm()
        return render(request, 'posts/add_post.html', {'form': form})
    else:
        return redirect('posts:all_post')


@login_required
def delete_post(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, 'delete post successfully')
        return redirect('account:user_dashboard', user_id)
    else:
        return redirect('posts:all_post')


@login_required
def edit_post(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, pk=post_id)
        if request.method == 'POST':
            form = EditPostForm(request.POST, instance=post)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.slug = slugify(form.cleaned_data.get('body'[:30]))
                new_form.save()
                messages.success(request, 'Edit post successfully')
                return redirect('account:user_dashboard', user_id)
        else:
            form = EditPostForm(instance=post)
        return render(request, 'posts/edit_post.html', {'form':form})
    else:
        return redirect('posts:all_post')