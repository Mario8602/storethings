from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'photo', Product.trim20, 'created_at', 'updated_at', 'price', 'amount', 'private']
    list_filter = ['created_at', 'updated_at', 'price', 'private']
    list_editable = ['price', 'amount', 'private']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
