from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))

    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))

    email = forms.EmailField(max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))

    password1 = forms.CharField(label='password', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    password2 = forms.CharField(label='Confirm password', max_length=100,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username__exact=username)
        if user.exists():
            raise forms.ValidationError('Username is Already. Try Again!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email__exact=email)
        if user.exists():
            raise forms.ValidationError('Email is Already. Try Again!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError('Password must be Match.')


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('bio', 'age')


class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        profile = Profile.objects.filter(phone__exact=phone)
        if not profile.exists():
            raise forms.ValidationError('Phone number not exists')
        return self.cleaned_data.get('phone')


class VerifyLoginForm(forms.Form):
    code = forms.IntegerField()