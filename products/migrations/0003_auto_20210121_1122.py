# Generated by Django 3.1.5 on 2021-01-21 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210117_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimages',
            options={'verbose_name': 'Product Image', 'verbose_name_plural': 'Products Images'},
        ),
    ]