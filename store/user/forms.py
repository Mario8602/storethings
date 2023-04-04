from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser
from .verify_acc import verify_acc_email


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

    # def clean(self):
    #     cleaned_data = super(CustomUserCreationForm, self).clean()
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['username']


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

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if not self.user_cache.email_verified:
                raise self.get_invalid_login_error()

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")
    #
    #     if username is not None and password:
    #         self.user_cache = authenticate(
    #             self.request,
    #             username=username,
    #             password=password
    #         )
    #         if not self.user_cache.email_verified:
    #             verify_acc_email(self.request, self.user_cache)
    #             raise ValidationError(
    #                 'Ваша почта не подтверждена. Пожалуйста, проверьте вашу электронную почту.',
    #                 code='invalid_login',
    #             )
    #         if self.user_cache is None:
    #             raise self.get_invalid_login_error()
    #         else:
    #             self.confirm_login_allowed(self.user_cache)
    #
    #     return self.cleaned_data

    # username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Имя профиля'
    # }))
    # password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Пароль'
    # }))
