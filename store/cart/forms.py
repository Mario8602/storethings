from django import forms
from .models import Order

PRODUCT_AMOUNT_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    amount = forms.TypedChoiceField(choices=PRODUCT_AMOUNT_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderAddForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['firstName', 'lastName', 'email', 'phoneNumber', 'postCode', 'city', 'address',]