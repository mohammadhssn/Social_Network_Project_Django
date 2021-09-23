from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Your logged in successfully', 'success')
                return redirect('posts:all_post')
            else:
                messages.warning(request, 'username or password wrong', 'warning')

    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})
