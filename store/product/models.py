from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class Category(models.Model):
    """ Наименование категории продукта """
    name = models.CharField(max_length=250, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=250, db_index=True)

    def get_absolute_url(self):
        return reverse('store:detail_of_prod_by_cat', args=[self.slug])

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """ Товары для продажи на сайте """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='prode')
    name = models.CharField(max_length=250, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=250, db_index=True, verbose_name='Слаг')
    photo = models.ImageField(upload_to='media/photos/%Y/%m/%d', blank=True)
    body = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    amount = models.PositiveIntegerField()
    private = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        # app_label = 'artek'

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.pk, self.slug])

    def __str__(self):
        return f'{self.name}'

    def trim20(self):
        return u"%s..." % (self.body[:50],)


class ProductDetails(models.Model):
    """ Дополнительная информация продуктов """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodDetail')
    uid = models.SmallIntegerField()