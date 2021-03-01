from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import User, Country, SiteInfo
from channels_presence.models import Room, Presence


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'birth_date', 'image')

    def name(self, obj):
        return obj.get_full_name()


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en', 'logo')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename')


admin.site.register(SiteInfo)
admin.site.register(ContentType)
admin.site.register(Room)
admin.site.register(Presence)

admin.site.site_header = "Ecommerce"
admin.site.site_title = "Ecommerce"
admin.site.index_title = "Ecommerce"
admin.site.login_template = "AdminLte/login.html"
