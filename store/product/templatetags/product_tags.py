from django import template

register = template.Library()

from ..models import Product


# @register.simple_tag
# def total_products():
#     return Product.objects.all(


@register.simple_tag
def total_products(category):
    num = Product.objects.filter(category__name=category).count()
    # worde = plural_word(str(category)).capitalize()
    if num % 10 == 1 and num != 11:
        return f"{num} товар"
    elif 2 <= num % 10 <= 4 and (not 12 <= num <= 14):
        return f"{num} товара"
    else:
        return f"{num} товаров"


# def plural_word(word):
#     vowels = ('а', 'о', 'и', 'е', 'э', 'ы', 'у', 'ю', 'я')
#     if word[-2:] == 'ия':
#         return word[:-2] + 'ии'
#     elif word[-1] == 'ь':
#         return word[:-1] + 'и'
#     elif word[-1] == 'й':
#         return word[:-1] + 'и'
#     elif word[-1] == 'а' and word[-3:-1] not in vowels:
#         return word[:-1] + 'ы'
#     elif word[-1] in vowels:
#         return word + 'ы'
#     else:
#         return word + 'ы'