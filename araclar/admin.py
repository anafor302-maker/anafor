from django.contrib import admin
from django.utils.html import format_html
from .models import SiteAyarlari, AracKategori, Arac, Rezervasyon

@admin.register(SiteAyarlari)
class SiteAyarlariAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Genel Ayarlar', {
            'fields': ('site_adi', 'site_aktif')
        }),
        ('SEO Ayarları', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Google Entegrasyonları', {
            'fields': ('google_analytics_id', 'google_ads_id', 'google_ads_conversion_label', 
                      'google_search_console_verification', 'gtm_id'),
            'description': 'Google Analytics, Ads ve Search Console kodlarınızı buraya girin.'
        }),
        ('İşletme Bilgileri (Schema.org)', {
            'fields': ('business_phone', 'business_email', 'business_address', 'opening_hours'),
            'classes': ('collapse',)
        }),
        ('Sosyal Medya', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url'),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        return not SiteAyarlari.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AracKategori)
class AracKategoriAdmin(admin.ModelAdmin):
    list_display = ['ad', 'sira', 'arac_sayisi']
    prepopulated_fields = {'slug': ('ad',)}
    
    def arac_sayisi(self, obj):
        return obj.araclar.count()
    arac_sayisi.short_description = 'Araç Sayısı'

@admin.register(Arac)
class AracAdmin(admin.ModelAdmin):
    list_display = ['gorsel_thumbnail', 'marka', 'model', 'yil', 'gunluk_fiyat', 'kategori', 'onerilir', 'aktif']
    list_filter = ['aktif', 'onerilir', 'kategori', 'yakit_tipi', 'vites_tipi']
    search_fields = ['marka', 'model']
    prepopulated_fields = {'slug': ('marka', 'model')}
    list_editable = ['onerilir', 'aktif']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('marka', 'model', 'slug', 'kategori', 'yil')
        }),
        ('Teknik Özellikler', {
            'fields': ('yakit_tipi', 'vites_tipi', 'koltuk_sayisi', 'bagaj_hacmi')
        }),
        ('Fiyatlandırma', {
            'fields': ('gunluk_fiyat', 'haftalik_fiyat', 'aylik_fiyat')
        }),
        ('Görseller', {
            'fields': ('ana_gorsel', 'gorsel_2', 'gorsel_3')
        }),
        ('SEO Ayarları', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'Boş bırakılırsa otomatik oluşturulur.'
        }),
        ('Durum', {
            'fields': ('aktif', 'onerilir')
        })
    )
    
    def gorsel_thumbnail(self, obj):
        if obj.ana_gorsel:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.ana_gorsel.url)
        return '-'
    gorsel_thumbnail.short_description = 'Görsel'

@admin.register(Rezervasyon)
class RezervasyonAdmin(admin.ModelAdmin):
    list_display = ['ad_soyad', 'arac', 'telefon', 'baslangic_tarihi', 'bitis_tarihi', 'olusturma_tarihi']
    list_filter = ['olusturma_tarihi', 'baslangic_tarihi']
    search_fields = ['ad_soyad', 'email', 'telefon']
    readonly_fields = ['olusturma_tarihi']
    date_hierarchy = 'olusturma_tarihi'