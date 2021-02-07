from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.exceptions import ObjectDoesNotExist


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
