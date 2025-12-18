from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class SiteAyarlari(models.Model):
    site_adi = models.CharField(max_length=200, default="Rent a Car")
    site_aktif = models.BooleanField(default=True, verbose_name="Site Aktif mi?")
    
    # SEO Meta
    meta_description = models.TextField(max_length=160, blank=True, help_text="Ana sayfa meta açıklaması (160 karakter)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Anahtar kelimeler (virgülle ayırın)")
    
    # Google Entegrasyonları
    google_analytics_id = models.CharField(max_length=50, blank=True, help_text="G-XXXXXXXXXX")
    google_ads_id = models.CharField(max_length=50, blank=True, help_text="AW-XXXXXXXXXX")
    google_ads_conversion_label = models.CharField(max_length=50, blank=True)
    google_search_console_verification = models.CharField(max_length=100, blank=True, help_text="Meta verification code")
    
    # Google Tag Manager
    gtm_id = models.CharField(max_length=50, blank=True, help_text="GTM-XXXXXXX", verbose_name="Google Tag Manager ID")
    
    # Schema.org Structured Data
    business_phone = models.CharField(max_length=20, blank=True, verbose_name="İşletme Telefonu")
    business_email = models.EmailField(blank=True, verbose_name="İşletme E-posta")
    business_address = models.TextField(blank=True, verbose_name="İşletme Adresi")
    opening_hours = models.CharField(max_length=100, blank=True, default="Mo-Su 09:00-18:00", verbose_name="Çalışma Saatleri")
    
    # Sosyal Medya (SEO için)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"
    
    def __str__(self):
        return self.site_adi
    
    def save(self, *args, **kwargs):
        if not self.pk and SiteAyarlari.objects.exists():
            raise ValueError("Yalnızca bir Site Ayarları kaydı olabilir!")
        super().save(*args, **kwargs)

class AracKategori(models.Model):
    ad = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    aciklama = models.TextField(blank=True)
    sira = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Araç Kategorisi"
        verbose_name_plural = "Araç Kategorileri"
        ordering = ['sira', 'ad']
    
    def __str__(self):
        return self.ad
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.ad, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('kategori_detay', kwargs={'slug': self.slug})

class Arac(models.Model):
    YAKIT_TIPLERI = [
        ('benzin', 'Benzin'),
        ('dizel', 'Dizel'),
        ('elektrik', 'Elektrik'),
        ('hibrit', 'Hibrit'),
    ]
    
    VITES_TIPLERI = [
        ('manuel', 'Manuel'),
        ('otomatik', 'Otomatik'),
    ]
    
    # Temel Bilgiler
    marka = models.CharField(max_length=100, verbose_name="Marka")
    model = models.CharField(max_length=100, verbose_name="Model")
    slug = models.SlugField(unique=True, blank=True)
    kategori = models.ForeignKey(AracKategori, on_delete=models.CASCADE, related_name='araclar')
    
    # Özellikler
    yil = models.IntegerField(verbose_name="Model Yılı")
    yakit_tipi = models.CharField(max_length=20, choices=YAKIT_TIPLERI)
    vites_tipi = models.CharField(max_length=20, choices=VITES_TIPLERI)
    koltuk_sayisi = models.IntegerField(default=5)
    bagaj_hacmi = models.IntegerField(help_text="Litre cinsinden", blank=True, null=True)
    
    # Fiyatlandırma
    gunluk_fiyat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Günlük Fiyat (TL)")
    haftalik_fiyat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Haftalık Fiyat (TL)")
    aylik_fiyat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Aylık Fiyat (TL)")
    
    # Görseller
    ana_gorsel = models.ImageField(upload_to='araclar/', verbose_name="Ana Görsel")
    gorsel_2 = models.ImageField(upload_to='araclar/', blank=True, null=True)
    gorsel_3 = models.ImageField(upload_to='araclar/', blank=True, null=True)
    
    # SEO
    meta_title = models.CharField(max_length=70, blank=True, help_text="Boş bırakılırsa otomatik oluşturulur")
    meta_description = models.TextField(max_length=160, blank=True, help_text="Boş bırakılırsa otomatik oluşturulur")
    
    # Durum
    aktif = models.BooleanField(default=True)
    onerilir = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Araç"
        verbose_name_plural = "Araçlar"
        ordering = ['-onerilir', '-olusturma_tarihi']
    
    def __str__(self):
        return f"{self.marka} {self.model} ({self.yil})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.marka}-{self.model}-{self.yil}", allow_unicode=True)
            self.slug = base_slug
        
        if not self.meta_title:
            self.meta_title = f"{self.marka} {self.model} Kiralama | {self.yil} Model"
        
        if not self.meta_description:
            self.meta_description = f"{self.marka} {self.model} araç kiralama. {self.yakit_tipi} yakıt, {self.vites_tipi} vites. Günlük {self.gunluk_fiyat} TL. Hemen rezervasyon yapın!"
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('arac_detay', kwargs={'slug': self.slug})

class Rezervasyon(models.Model):
    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    ad_soyad = models.CharField(max_length=200)
    email = models.EmailField()
    telefon = models.CharField(max_length=20)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()
    mesaj = models.TextField(blank=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    
    # Conversion tracking için
    conversion_tracked = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Rezervasyon"
        verbose_name_plural = "Rezervasyonlar"
        ordering = ['-olusturma_tarihi']
    
    def __str__(self):
        return f"{self.ad_soyad} - {self.arac}"