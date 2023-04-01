from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import OrderProd, Order
from product.models import Product

from .cart_methods import Cart
from .forms import CartAddProductForm, OrderAddForm
from .tasks import order_created


@require_POST
def cart_add(request, product_id):
    """ функции для работы с корзиной: добавление, удаление """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if product.amount != 0:
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            cart.add(product=product, amount=clean_data['amount'], update_amount=clean_data['update'])
        return redirect('cart:cart_detail')
    else:
        form = CartAddProductForm()
        messages.error(request, 'Нет в наличии!')
        return HttpResponseRedirect(product.get_absolute_url())


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})


def test_order(request):
    """ Создание заказа и его обработка """
    cart = Cart(request)
    order_form = OrderAddForm()
    if request.method == 'POST':
        order_form = OrderAddForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            for prod in cart:
                OrderProd.objects.create(order=order,
                                         product=prod['product'],
                                         price=prod['price'],
                                         amount=prod['amount'])
                Product.objects.filter(id=prod['product'].id).update(amount=F('amount') - 1)
            cart.clear()
            order_created.delay(order.id, order.email, order.firstName)
            return render(request, 'orders/success_order.html', {
                'order': order,
            })

    else:
        order_form = OrderAddForm()
    context = {
        'cart': cart,
        'order_form': order_form,
    }

    return render(request, 'orders/orders_create_form.html', context)


@staff_member_required
def order_detail_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/detail_for_admin.html', {'order': order})