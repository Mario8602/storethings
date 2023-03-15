from django.contrib import admin
from django.urls import path
from . import views

app_name = 'production'


urlpatterns = [
    path(r'', views.cart_detail, name='cart_detail'),
    path(r'add/<product_id>', views.cart_add, name='cart_add'),
    path(r'remove/<product_id>', views.cart_remove, name='cart_remove'),
    path(r'orderAdd/', views.test_order, name='order_add'),
    path(r'admin/order/<order_id>/', views.order_detail_admin, name='order_detail_admin'),
]