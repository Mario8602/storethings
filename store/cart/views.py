from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cart.models import OrderProd
from product.models import Product
from cart.tasks import order_created

from cart.cart_methods import Cart
from cart.forms import CartAddProductForm, OrderAddForm

""" функции для работы с корзиной: добавление, удаление """


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        cart.add(product=product, amount=clean_data['amount'], update_amount=clean_data['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})


""" Создание заказа и его обработка """


# def send(user_email, order_id):
#     send_mail(
#         'Вы подписались',
#         f'Ваш заказ номер {order_id} оформлен',
#         'Hellp8901@gmail.com',
#         [user_email],
#         fail_silently=False,
#     )


def test_order(request):

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
            cart.clear()
            order_created.delay(5, 10)
            # send('hellp8901@yandex.ru', order.id)
            return render(request, 'orders/success_order.html', {'order': order})

    else:
        order_form = OrderAddForm()

    context = {
        'cart': cart,
        'order_form': order_form,
    }

    return render(request, 'orders/order_create_form.html', context)



