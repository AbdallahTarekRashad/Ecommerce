from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.signals import user_logged_in


def add_cart_wish(sender, user, request, **kwargs):
    from products.models import Cart, WishList
    if request.session.exists(request.session.session_key):
        cart_session = Cart.objects.filter(session_key=request.session.session_key)
        wish_session = WishList.objects.filter(session_key=request.session.session_key)
        cart = Cart.objects.filter(user=user)
        wish = WishList.objects.filter(user=user)
        if cart_session:
            cart_session = cart_session.first()
            if cart and cart.first().products.count() > 0:
                cart = cart.first()
                plist = []
                for p in cart.products.all():
                    plist.append(p.product)
                for p in cart_session.products.all():
                    if p.product not in plist:
                        p.cart = cart
                        p.save()
                cart_session.delete()
            else:
                if cart:
                    cart.first().delete()
                cart_session.user = user
                cart_session.session_key = None
                cart_session.save()
        if wish_session:
            wish_session = wish_session.first()
            if wish and wish.first().products.count() > 0:
                wish = wish.first()
                for p in wish_session.products.all():
                    if p not in wish.products.all():
                        wish.products.add(p)
                wish.save()
                wish_session.delete()
            else:
                if wish:
                    wish.first().delete()
                wish_session.user = user
                wish_session.session_key = None
                wish_session.save()


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
