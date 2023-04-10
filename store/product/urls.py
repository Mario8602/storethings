from django.contrib import admin
from django.urls import path

from .views import products_by_category, product_detail, SearchResultView

app_name = 'prod'

urlpatterns = [
    path(r'', products_by_category, name='prod_list'),
    path(r'<category_slug>', products_by_category, name='detail_of_prod_by_cat'),
    path(r'<int:id>/<slug>', product_detail, name='product_detail'),
    path(r'search/', SearchResultView.as_view(), name='search_result'),
]