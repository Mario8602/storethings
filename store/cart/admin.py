import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import OrderProd, Order


# def export_to_csv(self, request, queryset):
#     meta = self.model._meta
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename={meta.verbose_name}.csv'
#     writer = csv.writer(response)
#     fields = [field for field in meta.get_fields() if not field.many_to_many and not field.one_to_many]
#     writer.writerow([field.verbose_name for field in fields])
#     for obj in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(obj, field.name)
#             if isinstance(value, datetime.datetime):
#                 value = value.strftime('%D/%M/%Y')
#             data_row.append(value)
#         writer.writerow(data_row)
#     return response
#
# export_to_csv.short_description = 'Export to CSV'

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
    list_display = ('firstName', 'lastName', 'email', 'city', 'created_at', 'payment')
    verbose_name = 'portrait'
    inlines = [OrderProdInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)


