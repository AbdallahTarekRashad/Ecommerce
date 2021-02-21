from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class ViewManager(models.Manager):
    def get_queryset(self):
        return super(ViewManager, self).get_queryset().filter(Q(stock__gte=1) & Q(publish=True))


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
    ENABLED = 0
    DISABLED = 1
    FREE = 2
    SIPPING_TYPE = [(ENABLED, _('Enabled')),
                    (DISABLED, _('Disabled')),
                    (FREE, _('Free')), ]

    sku = models.CharField(max_length=200, unique=True, verbose_name=_('SKU'),
                           help_text=_(
                               'Product stock keeping unit (SKU). Your internal unique identifier that can be used to '
                               'track this product.'))
    name = models.CharField(max_length=200, verbose_name=_('Name'), help_text=_('Name In English'))
    name_ar = models.CharField(max_length=200, verbose_name=_('Name Ar'), help_text=_('Name In Arabic'))
    price = models.PositiveIntegerField(verbose_name=_('Price'), help_text=_('Actual Price'))
    old_price = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Old Price'),
                                            help_text=_(
                                                'The old price of the product. If you set an old price, this will '
                                                'display alongside the current price on the product page to show the '
                                                'difference in price.'))
    product_cost = models.PositiveIntegerField(verbose_name=_('Product Cost'), help_text=_(
        'Product cost is a prime product cost. This field is only for internal use, not visible for customers.'))
    description = models.TextField(max_length=500, verbose_name=_('Description'),
                                   help_text=_(
                                       'Full description is the text that is displayed in product page in english.'))
    description_ar = models.TextField(max_length=500, verbose_name=_('Description Ar'), help_text=_(
        'Full description is the text that is displayed in product page in arabic.'))
    main_image = models.ImageField(upload_to='product/', verbose_name=_('Main Image'),
                                   help_text=_('Main image of product'))
    stock = models.PositiveIntegerField(verbose_name=_('Stock'), help_text=_('Product stock in store'))
    categories = models.ManyToManyField(Category, related_name='products', verbose_name=_('Categories'),
                                        help_text=_('Choose categories.you can choice more than one'))
    options = models.ManyToManyField(Option, related_name='products', verbose_name=_('Options'),
                                     help_text=_('Choose options.you can choice more than one'))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, related_name='products',
                              verbose_name=_('Brand'), help_text=_('Choose brand'))
    publish = models.BooleanField(default=True, verbose_name=_('Publish'), help_text=_(
        'Check to publish this product (visible in store). Uncheck to unpublished (product not available in store).'))
    show_on_home_page = models.BooleanField(default=False, verbose_name=_('Show on home page'), help_text=_(
        "Check to display this product on your store's home page. Recommended for your most popular products."))
    rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    rate_count = models.PositiveIntegerField(default=0)
    disable_buy_button = models.BooleanField(default=False, verbose_name=_('Disable Buy Button'),
                                             help_text=_(
                                                 "Check to disable the buy button for this product. This may be "
                                                 "necessary for products that are 'available upon request'."))
    available_upon_request = models.BooleanField(default=False, verbose_name=_('Available Upon Request'),
                                                 help_text=_('Check if this item is available for Pre-Order. It also '
                                                             'displays Pre-order button instead of Add to cart.'))
    not_returnable = models.BooleanField(default=False, verbose_name=_('Not Returnable'),
                                         help_text=_("Check if this product is not returnable. In this case a "
                                                     "customer won't be allowed to submit return request."))
    new = models.BooleanField(default=False, verbose_name=_('Mark As New'), help_text=_(
        'Check to mark the product as new. Use this option for promoting new products.'))
    admin_comment = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('Admin Comment'),
                                     help_text=_('This comment is for internal use only, not visible for customers.'))
    additional_shipping_charge = models.PositiveIntegerField(null=True, blank=True,
                                                             verbose_name=_('Additional Shipping Charge'),
                                                             help_text=_('The additional shipping charge.'))
    shipping_type = models.SmallIntegerField(choices=SIPPING_TYPE, default=0, verbose_name=_('Shipping Type'),
                                             help_text=_('Check if the product can be shipped'))
    weight = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Weight'))
    length = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Length'))
    width = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Width'))
    height = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Height'))

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
