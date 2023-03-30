from django.contrib import admin
from .models import Category, Product, LaptopDetails, MonitorDetails, KeyboardDetails, VideoCardDetails


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'photo', Product.trim20, 'created_at', 'updated_at', 'price', 'amount', 'private']
    list_filter = ['created_at', 'updated_at', 'price', 'private']
    list_editable = ['price', 'amount', 'private']
    list_display_links = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(LaptopDetails)
class LaptopDetailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'uid', 'model', 'color', 'operating_system']
    list_filter = ['product', 'model', 'operating_system']


@admin.register(MonitorDetails)
class MonitorDetailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'category', 'uid', 'model', 'color', 'frequency']
    list_filter = ['product', 'model', 'frequency']
    raw_id_fields = ['product', ]


@admin.register(KeyboardDetails)
class KeyboardDetailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'model', 'color']
    list_filter = ['product', 'model', 'color']
    raw_id_fields = ['product', ]


@admin.register(VideoCardDetails)
class VideoCardDetailsAdmin(admin.ModelAdmin):
    list_display = ['product', 'model', 'color']
    list_filter = ['product', 'model', 'color']
    raw_id_fields = ['product', ]
