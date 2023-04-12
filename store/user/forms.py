from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
# from .verify_acc import verify_acc_email
from cart.tasks import verify_acc_email


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
        fields = ('username', 'email', 'phone_number', 'email_verified', 'first_name', 'last_name')


User = get_user_model()


class LoginForm(AuthenticationForm):

    username = forms.CharField(label='Введите логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя профиля'
    }))
    password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтверждение пароля'
    }))

    error_messages = {
        "invalid_login": _(
            "Неверный логин или пароль. Пожалуйста, попробуйте снова."
        ),
        "inactive": _("Этот аккаунт не активен"),
        "not_confirmed": _("Ваш аккаунт не подтверждён")
    }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

            if not self.user_cache.email_verified:
                current_site = get_current_site(self.request)
                user_mail = self.user_cache.email
                context = {
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(self.user_cache.pk)),
                    "user": self.user_cache,
                    "token": token_generator.make_token(self.user_cache),
                }
                message = render_to_string(
                    'verify_email.html',
                    context=context,
                )
                verify_acc_email.delay(message, user_mail)

                raise ValidationError(
                    self.error_messages["not_confirmed"],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field.verbose_name},
        )