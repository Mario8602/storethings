import django_filters
from .models import Product, MonitorDetails


class ProductFilter(django_filters.FilterSet):
    # price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    # category__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price',]


class MonitorFilter(django_filters.FilterSet):

    class Meta:
        model = MonitorDetails
        fields = ['color', 'frequency', 'brightness', 'width']