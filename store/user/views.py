from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages


from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser
from cart.tasks import verify_acc_email
from cart.models import Order, OrderProd


def register_user(request):
    """ Регистрация пользователей на сайте """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request) # Возвращает текущий сайт
            user_mail = user.email
            context = {
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
            }
            message = render_to_string(
                'verify_email.html',
                context=context,
            )

            verify_acc_email.delay(message, user_mail) # отправка сообщения на почту со ссылкой подтверждения
            return redirect('users:confirm_email')
        else:
            messages.error(request, 'Ошибка при регистрации.')
    form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {"form_signup": form})


class MyLoginView(LoginView):
    """ Представление входа на сайт"""
    form_class = LoginForm


def logout_user(request):
    """ Представление выхода из профиля """
    logout(request)
    redirect('/')


class ShowProfilePageView(DetailView):
    """ Представление профиля пользователя """
    model = CustomUser
    template_name = 'profile_user.html'

    # def get_context_data(self, *args, **kwargs):
    #     users = CustomUser.objects.all()
    #     context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
    #     page_user = get_object_or_404(CustomUser, id=self.kwargs['pk'])
    #     context['page_user'] = page_user
    #     return context


User = get_user_model()


class EmailVerifyView(View):
    """ Представление верификации почты пользователя
    при переходе по ссылки, отправленной на почту."""
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verified = True # Присваивает полю email_verified значение True. Подтверждение аккаунта.
            user.save()
            login(request, user)
            return redirect('prod:prod_list')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestingr
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user


def purchase_history(request, pk):
    """ История покупок в профили пользователя """
    user = get_object_or_404(CustomUser, pk=pk)
    orders = Order.objects.filter(buyer=user.pk)
    orders_main = []
    for i in orders:
        orders_main += list(OrderProd.objects.filter(order=i))
    context = {
        'user': user,
        'orders': orders,
        'orders_main': orders_main,
    }
    return render(request, 'purchase_history.html', context=context)