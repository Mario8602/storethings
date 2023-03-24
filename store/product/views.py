from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .filters import ProductFilter, MonitorFilter
from cart.forms import CartAddProductForm
from .models import Category, Product, MonitorDetails, LaptopDetails


def products_by_category(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.all().order_by('?')
    # pagination = Paginator(products, 6)

    filter_product_mon = MonitorFilter(request.GET, queryset=MonitorDetails.objects.all())

    filter_product = ProductFilter(request.GET, queryset=Product.objects.all())
    pagination = Paginator(filter_product.qs, 4)

    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)
    category_now = None

    if category_slug:
        if category_slug == "monitor":
            category_now = category_slug
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            filter_product_mon = MonitorFilter(request.GET, queryset=MonitorDetails.objects.all())
            pagination = Paginator(filter_product_mon.qs, 4)

            page_number = request.GET.get('page')
            page_obj = pagination.get_page(page_number)
        else:
            category_now = category_slug
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            filter_product = ProductFilter(request.GET, queryset=Product.objects.filter(category=category))
            # filter_product_monitor = ProductFilter(request.GET, queryset=)
            # filter_product = filter_product.qs.filter(category=category)
            # pagination = Paginator(products, 3)
            pagination = Paginator(filter_product.qs, 4)

            page_number = request.GET.get('page')
            page_obj = pagination.get_page(page_number)

        # page_number = request.GET.get('page')
        # page_obj = pagination.get_page(page_number)

    context = {
        'category_now': category_now,
        'filter_mon': filter_product_mon,
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

    context = {
        'product': one_product,
        'cart_product_form': cart_product_form,
        'monitor': monitor,
        'laptop': laptop,
    }

    return render(request, 'detail.html', context)

