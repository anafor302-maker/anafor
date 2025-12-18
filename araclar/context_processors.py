from .models import SiteAyarlari

def site_settings(request):
    try:
        ayarlar = SiteAyarlari.objects.first()
    except:
        ayarlar = None
    return {'site_ayarlari': ayarlar}