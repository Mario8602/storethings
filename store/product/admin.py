from django.contrib import admin
from .models import Category, Product, LaptopDetails, MonitorDetails


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'photo', Product.trim20, 'created_at', 'updated_at', 'price', 'amount', 'private']
    list_filter = ['created_at', 'updated_at', 'price', 'private']
    list_editable = ['price', 'amount', 'private']
    prepopulated_fields = {'slug': ('name',)}


class LaptopDetailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'uid', 'model', 'color', 'operating_system']
    list_filter = ['product', 'model', 'operating_system']


class MonitorDetailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'category', 'uid', 'model', 'color', 'frequency']
    list_filter = ['product', 'model', 'frequency']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(LaptopDetails, LaptopDetailsAdmin)
admin.site.register(MonitorDetails, MonitorDetailsAdmin)
