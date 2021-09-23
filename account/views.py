from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post


# Create your views here.

def user_login(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Your logged in successfully', 'success')
                if next_url:
                    return redirect(next_url)
                return redirect('posts:all_post')
            else:
                messages.warning(request, 'username or password wrong', 'warning')

    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            login(request, user)
            messages.success(request, 'Your Register and logged in successfully', 'success')
            return redirect('posts:all_post')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Your Register and logged in successfully', 'success')
    return redirect('posts:all_post')


@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, pk__exact=user_id)
    posts = Post.objects.filter(user=user)
    self_dash = False
    if request.user.id == user.id:
        self_dash = True
    return render(request, 'account/user_dashboard.html', {'user':user, 'posts':posts, 'self_dash':self_dash})
