from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Arac, AracKategori, Rezervasyon, SiteAyarlari
from .forms import RezervasyonForm

def anasayfa(request):
    araclar = Arac.objects.filter(aktif=True)
    onerilir_araclar = araclar.filter(onerilir=True)[:6]
    tum_araclar = araclar[:12]
    kategoriler = AracKategori.objects.all()
    
    context = {
        'onerilir_araclar': onerilir_araclar,
        'tum_araclar': tum_araclar,
        'kategoriler': kategoriler,
    }
    return render(request, 'anasayfa.html', context)

def arac_listesi(request):
    araclar = Arac.objects.filter(aktif=True)
    
    kategori_slug = request.GET.get('kategori')
    if kategori_slug:
        araclar = araclar.filter(kategori__slug=kategori_slug)
    
    yakit = request.GET.get('yakit')
    if yakit:
        araclar = araclar.filter(yakit_tipi=yakit)
    
    vites = request.GET.get('vites')
    if vites:
        araclar = araclar.filter(vites_tipi=vites)
    
    sira = request.GET.get('sira', 'guncel')
    if sira == 'ucuz':
        araclar = araclar.order_by('gunluk_fiyat')
    elif sira == 'pahali':
        araclar = araclar.order_by('-gunluk_fiyat')
    
    paginator = Paginator(araclar, 12)
    sayfa = request.GET.get('sayfa')
    araclar_sayfa = paginator.get_page(sayfa)
    
    context = {
        'araclar': araclar_sayfa,
        'kategoriler': AracKategori.objects.all(),
    }
    return render(request, 'arac_listesi.html', context)

def arac_detay(request, slug):
    arac = get_object_or_404(Arac, slug=slug, aktif=True)
    benzer_araclar = Arac.objects.filter(kategori=arac.kategori, aktif=True).exclude(id=arac.id)[:4]
    
    conversion_data = None
    if request.method == 'POST':
        form = RezervasyonForm(request.POST)
        if form.is_valid():
            rezervasyon = form.save(commit=False)
            rezervasyon.arac = arac
            rezervasyon.save()
            
            # Google Ads Conversion tracking için
            ayarlar = SiteAyarlari.objects.first()
            if ayarlar and ayarlar.google_ads_id and ayarlar.google_ads_conversion_label:
                conversion_data = {
                    'ads_id': ayarlar.google_ads_id,
                    'conversion_label': ayarlar.google_ads_conversion_label,
                    'value': float(arac.gunluk_fiyat),
                    'currency': 'TRY'
                }
            
            messages.success(request, 'Rezervasyon talebiniz alındı. En kısa sürede sizinle iletişime geçeceğiz.')
            return redirect('rezervasyon_tesekkur', rezervasyon_id=rezervasyon.id)
    else:
        form = RezervasyonForm()
    
    context = {
        'arac': arac,
        'benzer_araclar': benzer_araclar,
        'form': form,
        'conversion_data': conversion_data,
    }
    return render(request, 'arac_detay.html', context)

def kategori_detay(request, slug):
    kategori = get_object_or_404(AracKategori, slug=slug)
    araclar = Arac.objects.filter(kategori=kategori, aktif=True)
    
    paginator = Paginator(araclar, 12)
    sayfa = request.GET.get('sayfa')
    araclar_sayfa = paginator.get_page(sayfa)
    
    context = {
        'kategori': kategori,
        'araclar': araclar_sayfa,
    }
    return render(request, 'kategori_detay.html', context)

def rezervasyon_tesekkur(request, rezervasyon_id):
    rezervasyon = get_object_or_404(Rezervasyon, id=rezervasyon_id)
    
    # Conversion tracking (sadece bir kez)
    conversion_data = None
    if not rezervasyon.conversion_tracked:
        ayarlar = SiteAyarlari.objects.first()
        if ayarlar and ayarlar.google_ads_id and ayarlar.google_ads_conversion_label:
            conversion_data = {
                'ads_id': ayarlar.google_ads_id,
                'conversion_label': ayarlar.google_ads_conversion_label,
                'value': float(rezervasyon.arac.gunluk_fiyat),
                'currency': 'TRY'
            }
            rezervasyon.conversion_tracked = True
            rezervasyon.save()
    
    context = {
        'rezervasyon': rezervasyon,
        'conversion_data': conversion_data,
    }
    return render(request, 'rezervasyon_tesekkur.html', context)