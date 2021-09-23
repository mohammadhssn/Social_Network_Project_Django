from django.shortcuts import render, get_object_or_404
from .models import Post


def all_post(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_post.html', {'posts':posts})


def post_detail(request, post_id, slug):
    post = get_object_or_404(Post, pk=post_id, slug__exact=slug)
    return render(request, 'posts/post_detail.html', {'post':post})