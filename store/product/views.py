from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .filters import ProductFilter, MonitorFilter, LaptopFilter, KeyboardFilter, VideoCartFilter
from cart.forms import CartAddProductForm
from .models import Category, Product, MonitorDetails, LaptopDetails, KeyboardDetails, VideoCardDetails


def products_by_category(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.all().order_by('?')

    filter_product = ProductFilter(request.GET, queryset=Product.objects.all())
    pagination = Paginator(filter_product.qs, 4)

    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    if category_slug:
        if category_slug == "monitor":
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            filter_product = MonitorFilter(request.GET, queryset=MonitorDetails.objects.all())
            pagination = Paginator(filter_product.qs, 5)
        elif category_slug == 'noutbuk':
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            filter_product = LaptopFilter(request.GET, queryset=LaptopDetails.objects.all())
            pagination = Paginator(filter_product.qs, 4)
        elif category_slug == 'klaviatura':
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            filter_product = KeyboardFilter(request.GET, queryset=KeyboardDetails.objects.all())
            pagination = Paginator(filter_product.qs, 4)
        elif category_slug == 'videokarta':
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            filter_product = VideoCartFilter(request.GET, queryset=VideoCardDetails.objects.all())
            pagination = Paginator(filter_product.qs, 4)
        else:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            filter_product = ProductFilter(request.GET, queryset=Product.objects.filter(category=category))
            pagination = Paginator(filter_product.qs, 4)

        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)

    context = {
        'filter': filter_product,
        'category': category,
        'categories': categories,
        'products': products,
        'page_obj': page_obj,
    }

    return render(request, 'main.html', context)


def product_detail(request, id, slug):

    one_product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()

    monitors = MonitorDetails.objects.all()
    monitor = monitors.filter(product=one_product)

    laptop = LaptopDetails.objects.all()
    laptop = laptop.filter(product=one_product)

    keyboard = KeyboardDetails.objects.all()
    keyboard = keyboard.filter(product=one_product)

    context = {
        'product': one_product,
        'cart_product_form': cart_product_form,
        'monitor': monitor,
        'laptop': laptop,
        'keyboard': keyboard,
    }

    return render(request, 'detail.html', context)

