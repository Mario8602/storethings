# Generated by Django 4.1.1 on 2023-03-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_laptopdetails_monitordetails_delete_productdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laptopdetails',
            name='category',
        ),
        migrations.AlterField(
            model_name='laptopdetails',
            name='uid',
            field=models.SmallIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='monitordetails',
            name='uid',
            field=models.SmallIntegerField(unique=True),
        ),
    ]
