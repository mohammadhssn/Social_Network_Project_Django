from django.shortcuts import render
from .models import Post


def all_post(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_post.html', {'posts':posts})