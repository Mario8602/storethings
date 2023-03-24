# Generated by Django 4.1.1 on 2023-03-22 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_laptopdetails_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptopdetails',
            name='frequency',
            field=models.CharField(choices=[('No info', 'no information'), ('60', '60 ГЦ'), ('144', '144 ГЦ'), ('160', '160 ГЦ'), ('240', '240 ГЦ'), ('360', '360 ГЦ')], default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='laptopdetails',
            name='operating_system',
            field=models.CharField(choices=[('Windows 10 Home', 'HO'), ('Windows 10 PRO', 'PR'), ('Windows 11', 'AA'), ('Linux', 'LI'), ('Without OS', 'WO')], default='WO', max_length=300),
        ),
        migrations.AlterField(
            model_name='monitordetails',
            name='frequency',
            field=models.CharField(choices=[('No info', 'no information'), ('60', '60 ГЦ'), ('144', '144 ГЦ'), ('160', '160 ГЦ'), ('240', '240 ГЦ'), ('360', '360 ГЦ')], default=0, max_length=50),
        ),
    ]
