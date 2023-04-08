from django.db import models

from product.models import Product
from user.models import CustomUser


class Order(models.Model):
    """ Модель для хранения информации о заказе и заказчике """
    firstName = models.CharField(max_length=30, blank=True, null=False)
    lastName = models.CharField(max_length=30, blank=True, null=False)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12, blank=True, null=False)
    postCode = models.CharField(max_length=10, blank=True, null=False)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=250, default='', blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment = models.BooleanField(default=False)
    # buyer = models.CharField(blank=True, null=True)
    buyer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='buyer', blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.id}'

    def get_cost_total(self):
        return sum(item.get_cost() for item in self.item.all())

    # def phone_number(self, phoneNumber):
    #     result = re.match(r'(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
    #     phoneNumber)
    #     return


class OrderProd(models.Model):
    """ Модель для хранения информации о купленном товаре """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('price',)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.amount
