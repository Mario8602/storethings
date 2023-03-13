from decimal import Decimal
from django.conf import settings

from product.models import Product


class Cart(object):

    def __init__(self, request):
        """ Инициализация корзины """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняет пустую корзину
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, amount=1, update_amount=False):
        """ Добавить выбранный продукт в корзину """
        prod_id = str(product.id)
        # проверяет наличие ID товара в корзине, и если нет, добавляет
        if prod_id not in self.cart:
            self.cart[prod_id] = {'amount': 0, 'price': str(product.price)}
        if update_amount:
            self.cart[prod_id]['amount'] = amount
        else:
            self.cart[prod_id]['amount'] += amount
        self.save()

    def save(self):
        # Обновление сессии корзины
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """ Удаление продуктов из корзины """
        prod_id = str(product.id)
        if prod_id in self.cart:
            del self.cart[prod_id]
            self.save()

    def __iter__(self):
        """ Перебор элементов корзины и Получение продуктов из базы данных"""
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['amount']
            yield item

    def __len__(self):
        """ Количество товаров в корзине """
        return sum(item['amount'] for item in self.cart.values())

    def get_total_price(self):
        """ Общая стоимость товаров в корзине """
        return sum(Decimal(item['price']) * item['amount'] for item in self.cart.values())

    def clear(self):
        """ Удаление корзины из сессии """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True