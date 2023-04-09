import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import OrderProd, Order


def export_to_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


export_to_csv.short_description = 'Export to CSV'


class OrderProdInline(admin.TabularInline):
    model = OrderProd
    raw_id_fields = ('product',)
    list_display = ('order', 'product', 'price', 'amount')


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('firstName', 'lastName', 'email', 'city', 'created_at', 'payment', 'buyer')
    verbose_name = 'portrait'
    inlines = [OrderProdInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)


