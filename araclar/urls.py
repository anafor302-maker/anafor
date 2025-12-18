from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('araclar/', views.arac_listesi, name='arac_listesi'),
    path('arac/<slug:slug>/', views.arac_detay, name='arac_detay'),
    path('kategori/<slug:slug>/', views.kategori_detay, name='kategori_detay'),
    path('tesekkurler/<int:rezervasyon_id>/', views.rezervasyon_tesekkur, name='rezervasyon_tesekkur'),
]
