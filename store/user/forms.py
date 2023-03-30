from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Введите логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя профиля'
    }))
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите адрес эл. почты'
    }))
    phone_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите номер телефона',
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Создайте пароль'
    }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтверждение пароля'
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Введите логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя профиля'
    }))
    password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтверждение пароля'
    }))
    # username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Имя профиля'
    # }))
    # password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Пароль'
    # }))
