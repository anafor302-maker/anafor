from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from araclar.sitemaps import AracSitemap, KategoriSitemap

sitemaps = {
    'araclar': AracSitemap,
    'kategoriler': KategoriSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('araclar.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin panel özelleştirme
admin.site.site_header = "Rent a Car Yönetim Paneli"
admin.site.site_title = "Rent a Car Admin"
admin.site.index_title = "Hoş Geldiniz"