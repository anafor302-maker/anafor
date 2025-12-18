from django import forms
from .models import Rezervasyon

class RezervasyonForm(forms.ModelForm):
    class Meta:
        model = Rezervasyon
        fields = ['ad_soyad', 'email', 'telefon', 'baslangic_tarihi', 'bitis_tarihi', 'mesaj']
        widgets = {
            'ad_soyad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız Soyadınız'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta Adresiniz'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0555 555 55 55'}),
            'baslangic_tarihi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bitis_tarihi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mesaj': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ek notlarınız...'}),
        }