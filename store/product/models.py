from random import choices

from django.db import models
from django.urls import reverse


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
        ('Нет информации', 'no info'),
        ('Чёрный', 'Black'),
        ('Белый', 'White'),
        ('Зелёный', 'Green'),
        ('Красный', 'Red'),
        ('Синий', 'Blue'),
        ('Жёлтый', 'Yellow'),
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
    uid = models.SmallIntegerField(unique=True, verbose_name='Уникальный идентификатор')
    model = models.CharField(max_length=250, null=True, blank=True, verbose_name='Модель')
    color = models.CharField(max_length=40, null=True, blank=True, verbose_name='Цвет')
    operating_system = models.CharField(max_length=50, choices=CHOICE_OS, default='No info', verbose_name='Операционная система')
    screen_type = models.CharField(max_length=50, choices=CHOICE_SCREEN_TYPE, default='No info', verbose_name='Тип матрицы монитора')
    screen_resolution = models.CharField(max_length=20, null=True, blank=True, verbose_name='Разрешение экрана')
    frequency = models.CharField(max_length=50, choices=CHOICE_FREQUENCY, default='No info', verbose_name='Частота')
    width = models.FloatField(null=True, blank=True, verbose_name='Ширина')
    depth = models.FloatField(null=True, blank=True, verbose_name='Глубина')
    weight = models.FloatField(null=True, blank=True, verbose_name='Вес ноутбука')

    class Meta:
        ordering = ('product', 'uid')

    def __str__(self):
        return self.model


class MonitorDetails(models.Model):
    """ Детальная информация мониторов """
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
    uid = models.SmallIntegerField(unique=True, verbose_name='Уникальный идентификатор')
    model = models.CharField(max_length=250, null=True, blank=True, verbose_name='Модель')
    color = models.CharField(max_length=40, null=True, blank=True, verbose_name='Цвет')
    diagonal = models.FloatField(null=True, blank=True, verbose_name='Диагональ экрана')
    resolution = models.CharField(max_length=20, null=True, blank=True, verbose_name='Разрешение')
    brightness = models.IntegerField(null=True, blank=True, verbose_name='Яркость')
    frequency = models.CharField(max_length=50, choices=CHOICE_FREQUENCY, default='0', verbose_name='Частота обновления')
    connector_VGA = models.BooleanField(default=False, verbose_name='Разъём VGA')
    connector_HDMI = models.BooleanField(default=False, verbose_name='Разъём HDMI')
    width = models.FloatField(null=True, blank=True, verbose_name='Ширина монитора')
    height = models.FloatField(null=True, blank=True, verbose_name='Высота без подставки')
    weight = models.FloatField(null=True, blank=True, verbose_name='Вес монитора')

    def __str__(self):
        return self.model


def add_uniq_uid():
    symbol_uuid = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    uid_list = choices(symbol_uuid, k=14)
    result = ''.join(uid_list)
    return result


class KeyboardDetails(models.Model):
    """ Детальная информация клавиатур """

    CHOICE_COLOR = (
        ('Нет информации', 'no info'),
        ('Чёрный', 'Black'),
        ('Белый', 'White'),
        ('Зелёный', 'Green'),
        ('Красный', 'Red'),
        ('Синий', 'Blue'),
        ('Жёлтый', 'Yellow'),
    )

    KEYCAP_MATERIAL_CHOICE = (
        ('no info', 'no info'),
        ('PBT', 'Polybutylene terephthalate'),
        ('ABS ', 'Acrylonitrile butadiene styrene'),
    )

    KEYBOARD_TYPE_CHOICE = (
        ('no info', 'no info'),
        ('Мембранная', 'Мембранная'),
        ('Резиновая', 'Резиновая'),
        ('Механическая', 'Механическая'),
        ('Оптическая', 'Оптическая'),
    )

    CASE_MATERIAL_CHOICE = (
        ('no info', 'no info'),
        ('Пластик', 'Plastic'),
        ('Алюминий', 'Aluminum'),
    )

    CONNECTION_CHOICE = (
        ('no info', 'no info'),
        ('USB', 'USB'),
        ('PS/2', 'PS/2'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='KeyboardDetails')
    uid = models.CharField(max_length=14, default=add_uniq_uid, unique=True)
    # Классификация
    model = models.CharField(max_length=200, verbose_name='Модель')
    keyboard_type = models.CharField(max_length=100, choices=KEYBOARD_TYPE_CHOICE, default='No info', verbose_name='Тип клавиатуры')
    # Внешний вид
    color = models.CharField(max_length=20, choices=CHOICE_COLOR, default='no info', verbose_name='Цвет')
    key_backlight = models.BooleanField(default=False, verbose_name='Подсветка клавиш')
    # Клавиши
    keycap_material = models.CharField(max_length=20, choices=KEYCAP_MATERIAL_CHOICE, default='no info', verbose_name='Материал кейкапов')
    total_number_of_keys = models.IntegerField(default=0, verbose_name='Количество клавиш')
    # Функциональность
    function_key = models.BooleanField(default=False, verbose_name='Клавиша функции')
    programmable_keys = models.BooleanField(default=False, verbose_name='Программируемые клавиши')
    # Конструкция
    case_material = models.CharField(max_length=20, choices=CASE_MATERIAL_CHOICE, default='no info', verbose_name='Материал корпуса')
    water_protection = models.BooleanField(default=False, verbose_name='Защита от воды')
    connection = models.CharField(max_length=20, choices=CONNECTION_CHOICE, default='no info', verbose_name='Интерфейс подключения')

    def __str__(self):
        return self.model


class VideoCardDetails(models.Model):
    """ Детальная информация по видеокартам """

    CHOICE_COLOR = (
        ('Нет информации', 'no info'),
        ('Чёрный', 'Black'),
        ('Белый', 'White'),
        ('Зелёный', 'Green'),
        ('Красный', 'Red'),
        ('Синий', 'Blue'),
        ('Жёлтый', 'Yellow'),
    )

    CHOICE_VIDEOMEMORY_SIZE = (
        ('Нет информации', 'no info'),
        ('4', '4 ГБ'),
        ('6', '6 ГБ'),
        ('8', '8 ГБ'),
    )

    CHOICE_MEMORY_TYPE = (
        ('no info', 'no info'),
        ('DDR3', 'DDR3'),
        ('GDDR3', 'GDDR3'),
        ('GDDR4', 'GDDR4'),
        ('GDDR5', 'GDDR5'),
        ('GDDR6', 'GDDR6'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='VideocardDetails')
    uid = models.CharField(max_length=14, default=add_uniq_uid, unique=True, verbose_name='Уникальный идентификатор')
    # Общие параметры
    model = models.CharField(max_length=200, verbose_name='Модель')
    color = models.CharField(max_length=20, choices=CHOICE_COLOR, default='no info', verbose_name='Цвет')
    # Основные параметры
    gpu = models.CharField(max_length=200, default='no info', verbose_name='Графический процессор')
    microarchitecture = models.CharField(max_length=200, default='no info', verbose_name='Микроархитектура')
    # Спецификация видеопамяти
    videomemory_size = models.CharField(max_length=20, choices=CHOICE_VIDEOMEMORY_SIZE, default='no info', verbose_name='Размер видеопамяти')
    memory_type = models.CharField(max_length=20, choices=CHOICE_MEMORY_TYPE, default='no info', verbose_name='Тип памяти')
    # Спецификация видеопроцессора
    frequency_videochip = models.IntegerField(default='0', verbose_name='Штатная частота работы видеочипа')
    ray_tracing_support = models.BooleanField(default=False, verbose_name='Поддержка трассировки лучей')
    number_texture_units = models.IntegerField(default='0', verbose_name='Число текстурных блоков')
    # Вывод изображения
    video_connectors_displayport = models.BooleanField(default=False, verbose_name='видеоразъём displayport')
    video_connectors_hdmi = models.BooleanField(default=False, verbose_name='видеоразъём hdmi')
    # Габариты и вес
    length = models.IntegerField(default='0', verbose_name='Длина, мм')
    width = models.IntegerField(default='0', verbose_name='Ширина, мм')
    weight = models.IntegerField(default='0', verbose_name='Вес, г')

    def __str__(self):
        return self.model