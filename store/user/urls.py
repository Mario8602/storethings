from django.contrib import admin
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # path(r'signup/', views.SignUpView.as_view(), name='signup'),
    path(r'signup/', views.register_user, name='signup'),
    path(r'profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='profile'),
    path(r'login/', views.login_user, name='login'),
]