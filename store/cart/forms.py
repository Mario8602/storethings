from django import forms
from .models import Order

PRODUCT_AMOUNT_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    amount = forms.TypedChoiceField(choices=PRODUCT_AMOUNT_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderAddForm(forms.ModelForm):
    firstName = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Имя',
        'rows': 1,
    }))
    lastName = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Фамилия',
        'rows': 1,
    }))
    email = forms.EmailField(label='', widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Введите email',
        'rows': 1,
    }))
    postCode = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Введите ваш почтовый индекс',
        'rows': 1,
    }))
    city = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Введите ваш город',
        'rows': 1,
    }))
    address = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Введите ваш адрес',
        'rows': 1,
    }))

    class Meta:
        model = Order
        fields = ['phoneNumber',]