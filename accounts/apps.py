from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.signals import user_logged_in


def add_cart_wish(sender, user, request, **kwargs):
    from products.models import Cart, WishList, CartProduct, Product

    cart_session = request.session.get('cart', None)
    wish_session = request.session.get('wish', None)
    cart = Cart.objects.get_or_create(user=user)[0]
    wish = WishList.objects.get_or_create(user=user)[0]
    if cart_session:
        for c in cart_session:
            try:
                # because  cart and product_id is unique together and if add product more than one time just update
                # quantity
                CartProduct.objects.create(cart=cart, product_id=c['product_id'],
                                           quantity=c['quantity'])
            except:
                cart_product = CartProduct.objects.get(cart=cart, product_id=c['product_id'])
                cart_product.quantity = c['quantity']
                cart_product.save()
    if wish_session:
        ls = wish.products.all()
        for w in wish_session:
            product = Product.objects.get(pk=w)
            if product not in ls:
                wish.products.add(w)


def add_site_info(sender, **kwargs):
    from .models import SiteInfo

    try:
        info = SiteInfo.objects.all().first()
    except ObjectDoesNotExist:
        info = None
    if info is None:
        info = SiteInfo(
            name='name',
            name_ar='name_ar',
            address='address',
            address_ar='address_ar',
            email='email@email.com',
            phone='0123456789',
            facebook='www.facebook.com',
            twitter='www.twitter.com',
            instagram='www.instagram.com',
            linkedin='www.linkedin.com'
        )
        info.save()


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        post_migrate.connect(add_site_info, sender=self)
        user_logged_in.connect(add_cart_wish)
