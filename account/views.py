from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, EditProfileForm, PhoneLoginForm, VerifyLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import Profile
from random import randint
from kavenegar import *
from django.utils import timezone


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
    return render(request, 'account/user_dashboard.html', {'user': user, 'posts': posts, 'self_dash': self_dash})


@login_required
def edit_profile(request, user_id):
    if request.user.id == user_id:
        user = get_object_or_404(User, pk=user_id)
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user.profile)
            if form.is_valid():
                form.save()
                user.email = form.cleaned_data.get('email')
                user.save()
                messages.success(request, 'change Profile Successfully', 'success')
                return redirect('account:user_dashboard', user_id)
        else:
            form = EditProfileForm(instance=user.profile, initial={'email': user.email})
        return render(request, 'account/adit_profile.html', {'form': form})
    else:
        return redirect('posts:all_post')


def phone_login(request):
    if request.method == 'POST':
        global phone, rand_num
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone = f"0{form.cleaned_data.get('phone')}"
            rand_num = randint(10000, 99999)
            try:
                api = KavenegarAPI(
                    '6E39745035626359304A6275577A787A755041782F39553545493470444263417A57584F5348716D44556B3D')
                params = {
                    'sender': '',  # optional
                    'receptor': phone,  # multiple mobile number, split by comma
                    'message': rand_num,
                }
                response = api.sms_send(params)
                profile = get_object_or_404(Profile, phone=phone)
                profile.verify_code = rand_num
                now_time = timezone.now()
                exp_time = timezone.timedelta(minutes=2)
                profile.expire_code = now_time + exp_time
                profile.save()
                messages.success(request, 'code send Successfully', 'success')
                return redirect('account:verify_phone')
            except APIException as e:
                print(e)
            except HTTPException as e:
                print(e)
    else:
        form = PhoneLoginForm()
    return render(request, 'account/phone_login.html', {'form': form})


def verify_phone(request):
    if request.method == 'POST':
        try:
            profile = get_object_or_404(Profile, phone=phone)
            user = get_object_or_404(User, profile=profile)
        except NameError:
            return redirect('posts:all_post')
        form = VerifyLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if user.profile.expire_code < timezone.now():
                user.profile.verify_code = None
                user.profile.save()
                messages.warning(request, 'code is expire . Try Again', 'warning')
                return redirect('posts:all_post')
            elif code == user.profile.verify_code:
                login(request, user)
                user.profile.code_verify = None
                user.profile.save()
                messages.success(request, 'Logged in Successfully', 'success')
                return redirect('posts:all_post')
            else:
                messages.error(request, 'code is wrong', 'danger')
    else:
        form = VerifyLoginForm()
    return render(request, 'account/verify_phone.html', {'form': form})
