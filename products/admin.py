from django.contrib import admin
from .models import Product, Category, Option, ProductImages

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Option)
admin.site.register(ProductImages)
