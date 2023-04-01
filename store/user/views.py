from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView
from django.contrib import messages

from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'


def register_user(request):
    """ Регистрация пользователей на сайте """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # login(request, user)
            # messages.success(request, 'Успешная регистрация.')
            # return redirect('prod:prod_list')
        messages.error(request, 'Ошибка при регистрации.')
    form = CustomUserCreationForm()
    return render(request, 'signup.html', {"form_signup": form})


def login_user(request):
    """ Вход на сайт после регистрации """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    redirect('/')


class ShowProfilePageView(DetailView):
    model = CustomUser
    template_name = 'profile_user.html'

    def get_context_data(self, *args, **kwargs):
        users = CustomUser.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context
