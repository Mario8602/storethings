from django.contrib import admin

from cart.models import OrderProd, Order


class OrderProdInline(admin.TabularInline):
    model = OrderProd
    raw_id_fields = ('product',)
    list_display = ('order', 'product', 'price', 'amount')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email', 'city', 'created_at', 'payment')
    inlines = [OrderProdInline]


admin.site.register(Order, OrderAdmin)
