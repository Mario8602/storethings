# Generated by Django 4.1.1 on 2023-03-22 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_laptopdetails_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptopdetails',
            name='frequency',
            field=models.CharField(choices=[(0, 'No info'), (1, '60'), (2, '144'), (3, '160'), (4, '240'), (5, '360')], default=0, max_length=2),
        ),
        migrations.AddField(
            model_name='laptopdetails',
            name='screen_resolution',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='laptopdetails',
            name='screen_type',
            field=models.CharField(choices=[('0', 'No info'), ('1', 'IPS'), ('2', 'IGZO'), ('3', 'VA'), ('4', 'TN+Film'), ('5', 'OLED'), ('6', 'other')], default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='laptopdetails',
            name='operating_system',
            field=models.CharField(choices=[('HO', 'Windows 10 Home'), ('PR', 'Windows 10 PRO'), ('WI', 'Windows 11'), ('LI', 'Linux'), ('WO', 'Without OS')], default='WO', max_length=2),
        ),
        migrations.AlterField(
            model_name='monitordetails',
            name='frequency',
            field=models.CharField(choices=[(0, 'No info'), (1, '60'), (2, '144'), (3, '160'), (4, '240'), (5, '360')], default=0, max_length=2),
        ),
    ]