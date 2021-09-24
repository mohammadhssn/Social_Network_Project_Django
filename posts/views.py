from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.contrib import messages
from .models import Post, Comment, Like
from django.contrib.auth.decorators import login_required
from .forms import AddPostForm, EditPostForm, AddCommentForm, AddReplyForm


def all_post(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_post.html', {'posts': posts})


def post_detail(request, post_id, slug):
    post = get_object_or_404(Post, pk=post_id, slug__exact=slug)
    comments = Comment.objects.filter(post__exact=post, is_reply=False)
    reply_form = AddReplyForm()
    can_like = False
    if request.user.is_authenticated:
        if post.can_like(request.user):
            can_like = True
    if request.user.is_authenticated and request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.post = post
            new_form.save()
            messages.success(request, 'Add Comment successfully', 'success')
            return redirect('posts:post_detail', post_id, slug)
    else:
        form = AddCommentForm()
    return render(request, 'posts/post_detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'reply_form': reply_form, 'can_like': can_like})


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
                messages.success(request, 'Edit post successfully', 'success')
                return redirect('account:user_dashboard', user_id)
        else:
            form = EditPostForm(instance=post)
        return render(request, 'posts/edit_post.html', {'form': form})
    else:
        return redirect('posts:all_post')


@login_required
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'Reply post successfully', 'success')
            return redirect('posts:post_detail', post.id, post.slug)


@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like(user=request.user, post=post)
    like.save()
    messages.success(request, 'Like post successfully', 'success')
    return redirect('posts:post_detail', post.id, post.slug)


@login_required
def post_unlike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post)
    if like.exists():
        like.delete()
    messages.success(request, 'unLike post successfully', 'success')
    return redirect('posts:post_detail', post.id, post.slug)
