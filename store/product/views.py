from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from cart.forms import CartAddProductForm
from .models import Category, Product, MonitorDetails, LaptopDetails


def products_by_category(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    pagination = Paginator(products, 6)

    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        pagination = Paginator(products, 6)

        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'page_obj': page_obj,
    }

    return render(request, 'main.html', context)


def product_detail(request, id, slug):
    monitors = MonitorDetails.objects.all()
    # monitor = get_object_or_404(MonitorDetails)

    one_product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    # category = get_object_or_404(Category, slug=category_slug)

    monitor = monitors.filter(product=one_product)

    context = {
        'product': one_product,
        'cart_product_form': cart_product_form,
        # 'category': category,
        'monitor': monitor,
    }

    return render(request, 'detail.html', context)


# def product_detail_improved(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug)
#
#     context = {
#         'product': product,
#     }
#
#     return render(request, 'detail.html', context)
