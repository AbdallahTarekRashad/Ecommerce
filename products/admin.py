from django.contrib import admin
from .models import Product, Category, Option, ProductImages, Cart, WishList, ProductReview

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Option)
admin.site.register(ProductImages)
admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(ProductReview)
