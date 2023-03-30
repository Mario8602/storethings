import django_filters
from .models import Product, MonitorDetails, LaptopDetails, KeyboardDetails, VideoCardDetails


class ProductFilter(django_filters.FilterSet):
    # price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    # category__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price', ]


class MonitorFilter(django_filters.FilterSet):

    class Meta:
        model = MonitorDetails
        fields = ['color', 'frequency', 'brightness', 'width']


class LaptopFilter(django_filters.FilterSet):

    class Meta:
        model = LaptopDetails
        fields = ['color', 'screen_type', 'screen_resolution', 'frequency']


class KeyboardFilter(django_filters.FilterSet):
    # product__price = django_filters.RangeFilter()
    # class Meta:
    #     model = KeyboardDetails
    #     fields = ['product__price', 'color', 'key_backlight', 'keycap_material', 'programmable_keys', 'case_material', 'water_protection']

    class Meta:
        model = KeyboardDetails
        fields = {
            'product__price': ['lt', 'gt'],
            'color': ['exact'],
            'key_backlight': ['exact', 'contains'],
            'keycap_material': ['exact', 'contains'],
            'programmable_keys': ['contains'],
            'case_material': ['contains'],
            'water_protection': ['contains'],
        }


class VideoCartFilter(django_filters.FilterSet):

    class Meta:
        model = VideoCardDetails
        fields = ['color', 'videomemory_size', 'memory_type', 'frequency_videochip']
