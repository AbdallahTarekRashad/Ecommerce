from .models import SiteInfo


def site_info(request):
    info = SiteInfo.objects.all().first()
    return {'site_info': info}
