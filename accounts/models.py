from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField


# Create your models here.

class Country(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    logo = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.logo + ' ' + self.name_en + ' ' + self.name_ar



class User(AbstractUser):
    CUSTOMER = MALE = 0
    SELLER = FEMALE = 1
    TYPE = [(CUSTOMER, _('Customer')),
            (SELLER, _('Seller')), ]
    GENDER = [
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    ]
    birth_date = models.DateField(blank=True, null=True, verbose_name=_('Birth Date'))
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    billing_address = models.CharField(max_length=500, blank=True, null=True, verbose_name=_('Billing Address'))
    default_shipping_address = models.CharField(max_length=500, blank=True, null=True,
                                                verbose_name=_('Default Shipping Address'))
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT, related_name=_('users'),
                                verbose_name=_('Country'))
    phone = PhoneField(blank=True, null=True, verbose_name=_('Phone'))
    type = models.SmallIntegerField(choices=TYPE, default=0)
    gender = models.SmallIntegerField(choices=GENDER, blank=True, null=True)
    # to log with email
    # email overwrite to be unique
    # removed from required fields list
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class SiteInfo(models.Model):
    address = models.CharField(max_length=200, verbose_name=_('Address'))
    address_ar = models.CharField(max_length=200, verbose_name=_('Address Ar'))
    name = models.CharField(max_length=150, verbose_name=_('Name'))
    name_ar = models.CharField(max_length=150, verbose_name=_('Name Ar'))
    email = models.EmailField(verbose_name=_('Email'))
    phone = PhoneField(verbose_name=_('Phone'))
    phone2 = PhoneField(blank=True, null=True, verbose_name=_('Phone'))
    facebook = models.URLField(verbose_name=_('Facebook'), blank=True, null=True)
    twitter = models.URLField(verbose_name=_('Twitter'), blank=True, null=True)
    instagram = models.URLField(verbose_name=_('Instagram'), blank=True, null=True)
    linkedin = models.URLField(verbose_name=_('Linkedin'), blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', verbose_name=_('Logo'), default='/logo/download.jpeg')
    whatsapp_btn = models.BooleanField(default=True, verbose_name=_('Whats App'))

    class Meta:
        verbose_name = _('Site Info')
