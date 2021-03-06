# Generated by Django 3.1.5 on 2021-01-17 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='products', to='products.Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='options',
            field=models.ManyToManyField(related_name='products', to='products.Option'),
        ),
    ]
