from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, DetailView
from django.contrib import messages


from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser
# from .verify_acc import verify_acc_email
# from .tasks import verify_acc_email
from cart.tasks import verify_acc_email
from cart.models import Order, OrderProd


def register_user(request):
    """ Регистрация пользователей на сайте """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request)
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

            verify_acc_email.delay(message, user_mail)
            # verify_acc_email.delay(request, user)
            return redirect('users:confirm_email')
            # login(request, user)
            # messages.success(request, 'Успешная регистрация.')
            # return redirect('prod:prod_list')
        else:
            messages.error(request, 'Ошибка при регистрации.')
    form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {"form_signup": form})


# def login_user(request):
#     """ Вход на сайт после регистрации """
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('/')
#     else:
#         form = LoginForm()
#
#     return render(request, 'login.html', {'form': form})


class MyLoginView(LoginView):
    form_class = LoginForm


def logout_user(request):
    logout(request)
    redirect('/')


class ShowProfilePageView(DetailView):
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

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            login(request, user)
            return redirect('prod:prod_list')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
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
    # user = get_user_model()
    user = get_object_or_404(CustomUser, pk=pk)
    orders = Order.objects.filter(buyer=user.pk)
    # order = Order.objects.all()
    # orders_main = OrderProd.objects.filter(order_id=order.id)
    orders_main = []
    for i in orders:
        orders_main += list(OrderProd.objects.filter(order=i))
        # orders_main = get_object_or_404(OrderProd, order=i)

    context = {
        'user': user,
        'orders': orders,
        'orders_main': orders_main,
    }
    return render(request, 'purchase_history.html', context=context)