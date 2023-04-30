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


class CustomBooleanWidget(forms.Select):
    def __init__(self, *args, **kwargs):
        super(CustomBooleanWidget, self).__init__(*args, **kwargs)
        self.choices = [(None, 'Подсветка клавиш'), (True, 'Да'), (False, 'Нет')] + self.choices


class KeyboardFilter(django_filters.FilterSet):

    price__gt = django_filters.NumberFilter(
        label='',
        field_name='product__price',
        lookup_expr='gt',
        widget=forms.NumberInput(attrs={'class': 'adult-left price_cl', 'value': '0'}),
        help_text=' ---  ',
    )

    price__lt = django_filters.NumberFilter(
        label='',
        field_name='product__price',
        lookup_expr='lt',
        widget=forms.NumberInput(
            attrs={'class': 'adult-right price_cl', 'style': 'display: inline;', 'value': '99999'}
        ),
        help_text='   ---  ',
    )

    key_backlight = django_filters.BooleanFilter(
        label='Подсветка клавиш',
        widget=CustomBooleanWidget(attrs={
            'class': 'filter-form lb-form'
        }),
    )

    keyboard_type = django_filters.ChoiceFilter(
        choices=KeyboardDetails.KEYBOARD_TYPE_CHOICE,
        widget=forms.Select(attrs={
            'class': 'filter-form lb-form',
        }),
        empty_label=None
    )

    color = django_filters.ChoiceFilter(
        choices=KeyboardDetails.CHOICE_COLOR,
        widget=forms.Select(attrs={
            'class': 'filter-form lb-form',
        }),
        empty_label=None
    )

    class Meta:
        model = KeyboardDetails
        fields = ['key_backlight', 'price__gt', 'price__lt', 'keyboard_type']
        # fields = {
        #     'key_backlight': ['exact'],
        #     'keyboard_type': ['exact'],
        #     'product__price': ['lt', 'gt'],
        # }
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