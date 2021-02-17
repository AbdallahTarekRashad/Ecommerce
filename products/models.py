from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class ViewManager(models.Manager):
    def get_queryset(self):
        return super(ViewManager, self).get_queryset().filter(Q(stock__gte=1) & Q(show=True))


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Option(BaseModel):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    name_ar = models.CharField(max_length=200, verbose_name=_('name ar'))
    description = models.CharField(max_length=500, verbose_name=_('description'))
    description_ar = models.CharField(max_length=500, verbose_name=_('description ar'))

    class Meta:
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.name + ' ' + self.name_ar


class Category(BaseModel):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    name_ar = models.CharField(max_length=200, verbose_name=_('name ar'))
    description = models.CharField(max_length=500, verbose_name=_('description'))
    description_ar = models.CharField(max_length=500, verbose_name=_('description ar'))
    image = models.ImageField(upload_to='category/', verbose_name=_('image'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name + ' ' + self.name_ar


class Brand(BaseModel):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    name_ar = models.CharField(max_length=200, verbose_name=_('name ar'))
    description = models.CharField(max_length=500, verbose_name=_('description'))
    description_ar = models.CharField(max_length=500, verbose_name=_('description ar'))
    image = models.ImageField(upload_to='brand/', verbose_name=_('image'))

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name + ' ' + self.name_ar


class Product(BaseModel):
    sku = models.CharField(max_length=200, unique=True, verbose_name=_('sku'))
    name = models.CharField(max_length=200, verbose_name=_('name'))
    name_ar = models.CharField(max_length=200, verbose_name=_('name ar'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    weight = models.PositiveIntegerField(verbose_name=_('weight'))
    description = models.CharField(max_length=500, verbose_name=_('description'))
    description_ar = models.CharField(max_length=500, verbose_name=_('description ar'))
    main_image = models.ImageField(upload_to='product/', verbose_name=_('main image'))
    stock = models.PositiveIntegerField(verbose_name=_('stock'))
    categories = models.ManyToManyField(Category, related_name='products', verbose_name=_('categories'))
    options = models.ManyToManyField(Option, related_name='products', verbose_name=_('options'))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, related_name='products',
                              verbose_name=_('brand'))
    show = models.BooleanField(default=True, verbose_name=_('show'))
    rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    rate_count = models.PositiveIntegerField(default=0)
    objects = models.Manager()
    view_object = ViewManager()  # for Site Views

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name + ' ' + self.name_ar


# product have more than one image
class ProductImages(BaseModel):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images',
                                   verbose_name=_('product id'))
    image = models.ImageField(upload_to='product/', verbose_name=_('image'))

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Products Images')

    def __str__(self):
        return self.product_id.__str__()


class ProductReview(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], verbose_name='rate')
    comment = models.CharField(max_length=200, verbose_name='comment')

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self._state.adding is True:
            self.product.rate_count += 1
            self.product.rate = self.product.rate + (int(self.rate) - self.product.rate) / self.product.rate_count
            self.product.save()
        super(ProductReview, self).save(force_insert, force_update, using, update_fields)


class Cart(BaseModel):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='cart')
    session_key = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name=_('session key'))


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'), default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')

    class Meta:
        unique_together = ('product', 'cart',)


class WishList(BaseModel):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='wishlist')
    session_key = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name=_('session key'))
    products = models.ManyToManyField(Product, related_name='wishlist')
