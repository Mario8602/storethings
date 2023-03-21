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
        return u"%s..." % (self.body[:20],)


class LaptopDetails(models.Model):

    # CHOICE_OS = ['Windows 10 Home', 'Windows 10 PRO', 'Windows 11', 'Linux']
    CHOICE_OS = (
        ('HO', 'Windows 10 Home'),
        ('PR', 'Windows 10 PRO'),
        ('WI', 'Windows 11'),
        ('LI', 'Linux'),
    )

    CHOICE_COLOR = (
        ('BL', 'Black'),
        ('WH', 'White'),
        ('GR', 'Green'),
        ('RE', 'Red'),
        ('BL', 'Blue'),
        ('RE', 'Red'),
    )

    """ Дополнительная информация продуктов """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodDetail_1')
    # category = models.ForeignKey(Category, default='Электротехника', on_delete=models.SET_DEFAULT, related_name='category_productDetail_1')
    # category = models.ForeignKey(Category, choices=Product.category, default='Электротехника', on_delete=models.SET_DEFAULT)
    uid = models.SmallIntegerField(unique=True)
    model = models.CharField(max_length=250)
    color = models.CharField(max_length=40)
    operating_system = models.CharField(max_length=2, choices=CHOICE_OS, default='HO',)

    class Meta:
        ordering = ('product', 'uid')

    def __str__(self):
        return self.model


class MonitorDetails(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodDetail_2')
    category = models.ForeignKey(Category, default='Электротехника', on_delete=models.SET_DEFAULT, related_name='category_productDetail_2')
    uid = models.SmallIntegerField(unique=True)
    model = models.CharField(max_length=250)
    color = models.CharField(max_length=40)
    diagonal = models.FloatField()
    resolution = models.CharField(max_length=20)
    brightness = models.IntegerField()
    frequency = models.IntegerField()
    connector_VGA = models.BooleanField()
    connector_HDMI = models.BooleanField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.pk])

