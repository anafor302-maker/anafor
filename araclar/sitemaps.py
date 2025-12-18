from django.contrib.sitemaps import Sitemap
from .models import Arac, AracKategori

class AracSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    
    def items(self):
        return Arac.objects.filter(aktif=True)
    
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

class KategoriSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    
    def items(self):
        return AracKategori.objects.all()