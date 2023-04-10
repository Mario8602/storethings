from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q

from .filters import ProductFilter, MonitorFilter, LaptopFilter, KeyboardFilter, VideoCartFilter
from cart.forms import CartAddProductForm
from .models import Category, Product, MonitorDetails, LaptopDetails, KeyboardDetails, VideoCardDetails


def products_by_category(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.all().order_by('?')

    filter_product = ProductFilter(request.GET, queryset=Product.objects.all())
    pagination = Paginator(filter_product.qs, 8)

    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    if category_slug:

        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

        if category_slug == "monitor":
            filter_product = MonitorFilter(request.GET, queryset=MonitorDetails.objects.all())
            pagination = Paginator(filter_product.qs, 5)
        elif category_slug == 'noutbuk':
            filter_product = LaptopFilter(request.GET, queryset=LaptopDetails.objects.all())
            pagination = Paginator(filter_product.qs, 4)
        elif category_slug == 'klaviatura':
            filter_product = KeyboardFilter(request.GET, queryset=KeyboardDetails.objects.all())
            pagination = Paginator(filter_product.qs, 4)
        elif category_slug == 'videokarta':
            filter_product = VideoCartFilter(request.GET, queryset=VideoCardDetails.objects.all())
            pagination = Paginator(filter_product.qs, 4)
        else:
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

    videokarta = VideoCardDetails.objects.all()
    videokarta = videokarta.filter(product=one_product)

    context = {
        'product': one_product,
        'cart_product_form': cart_product_form,
        'monitor': monitor,
        'laptop': laptop,
        'keyboard': keyboard,
        'videokarta': videokarta,
    }

    return render(request, 'detail.html', context)


class SearchResultView(ListView):
    model = Product
    template_name = 'search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )
        return object_list
