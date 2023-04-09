from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import EmailVerifyView
from cart.models import Order

app_name = 'users'

urlpatterns = [
    # path(r'login/', views.login_user, name='login'),
    path(r'login/', views.MyLoginView.as_view(), name='login'),
    path(r'signup/', views.register_user, name='signup'),
    path(r'profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='profile'),
    path(r'confirm_email/', TemplateView.as_view(template_name='confirm_email.html'), name='confirm_email'),
    path(
            "verify_email/<uidb64>/<token>/",
            EmailVerifyView.as_view(),
            name="verify_email",
        ),
    path(r'invalid_verify/', TemplateView.as_view(template_name='invalid_verify.html'), name='invalid_verify'),
    path(r'profile/<int:pk>/archive/', views.purchase_history, name='archive')
]