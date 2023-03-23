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

    CHOICE_OS = [
        ('Windows 10 Home', 'Windows 10 home'),
        ('Windows 10 PRO', 'Windows 10 PRO'),
        ('Windows 11 home', 'Windows 11 home'),
        ('Windows 11 pro', 'Windows 11 pro'),
        ('Linux', 'Linux'),
        ('Mac OS', 'Mac OS'),
        ('Without OS', 'Without OS'),
    ]

    CHOICE_COLOR = (
        ('Black', 'Black'),
        ('White', 'White'),
        ('Green', 'Green'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Yellow', 'Yellow'),
    )

    CHOICE_SCREEN_TYPE = (
        ('No info', 'No info'),
        ('IPS', 'IPS'),
        ('IGZO', 'IGZO'),
        ('VA', 'VA'),
        ('TN+Film', 'TN+Film'),
        ('OLED', 'OLED'),
        ('other', 'other')
    )

    CHOICE_FREQUENCY = (
        ('No info', 'no information'),
        ('60', '60 ГЦ'),
        ('144', '144 ГЦ'),
        ('160', '160 ГЦ'),
        ('240', '240 ГЦ'),
        ('360', '360 ГЦ'),
    )

    """ Дополнительная информация продуктов """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodDetail_1')
    uid = models.SmallIntegerField(unique=True)
    model = models.CharField(max_length=250, null=True, blank=True)
    color = models.CharField(max_length=40, null=True, blank=True)
    operating_system = models.CharField(max_length=50, choices=CHOICE_OS, default='No info',)
    screen_type = models.CharField(max_length=50, choices=CHOICE_SCREEN_TYPE, default='0',)
    screen_resolution = models.CharField(max_length=20, null=True, blank=True)
    frequency = models.CharField(max_length=50, choices=CHOICE_FREQUENCY, default=0,)
    width = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ('product', 'uid')

    def __str__(self):
        return self.model


class MonitorDetails(models.Model):

    CHOICE_FREQUENCY = [
        ('No info', 'no information'),
        ('60', '60 ГЦ'),
        ('144', '144 ГЦ'),
        ('160', '160 ГЦ'),
        ('240', '240 ГЦ'),
        ('360', '360 ГЦ'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodDetail_2')
    category = models.ForeignKey(Category, default='Электротехника', on_delete=models.SET_DEFAULT, related_name='category_productDetail_2')
    uid = models.SmallIntegerField(unique=True)
    model = models.CharField(max_length=250, null=True, blank=True)
    color = models.CharField(max_length=40, null=True, blank=True)
    diagonal = models.FloatField(null=True, blank=True)
    resolution = models.CharField(max_length=20, null=True, blank=True)
    brightness = models.IntegerField(null=True, blank=True)
    frequency = models.CharField(max_length=50, choices=CHOICE_FREQUENCY, default=0)
    connector_VGA = models.BooleanField()
    connector_HDMI = models.BooleanField()
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.pk])

