from django.shortcuts import render
from .models import SiteAyarlari

class SiteActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        try:
            ayarlar = SiteAyarlari.objects.first()
            if ayarlar and not ayarlar.site_aktif:
                return render(request, 'site_kapali.html', status=503)
        except:
            pass
        
        return self.get_response(request)