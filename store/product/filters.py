from django import forms
import django_filters
# from django_filters.widgets import LookupChoiceWidget
from django_filters.widgets import BooleanWidget

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

    KEYBOARD_TYPE_CHOICE = (
        ('', 'Выберите тип клавиатуры'),
        ('Мембранная', 'Мембранная'),
        ('Резиновая', 'Резиновая'),
        ('Механическая', 'Механическая'),
        ('Оптическая', 'Оптическая'),
    )

    key_backlight = django_filters.BooleanFilter(
        label='Подсветка клавиш',
        widget=BooleanWidget(attrs={
            'class': 'md-textarea form-control lb-form',
        }),
    )
    keyboard_type = django_filters.ChoiceFilter(
        choices=KEYBOARD_TYPE_CHOICE,
        widget=forms.Select(attrs={
            'class': 'filter-form lb-form',
        }),
        empty_label=None
    )

    class Meta:
        model = KeyboardDetails
        fields = ['key_backlight', 'keyboard_type']
    #     fields = {
    #         'product__price': ['lt', 'gt'],
    #         'color': ['exact'],
    #         # 'key_backlight': ['exact',],
    #         'keycap_material': ['exact',],
    #         'programmable_keys': ['contains'],
    #         'case_material': ['contains'],
    #         'water_protection': ['contains'],
    #     }


class VideoCartFilter(django_filters.FilterSet):

    class Meta:
        model = VideoCardDetails
        fields = ['color', 'videomemory_size', 'memory_type', 'frequency_videochip']


# class FrequencyWidget(LookupChoiceWidget):