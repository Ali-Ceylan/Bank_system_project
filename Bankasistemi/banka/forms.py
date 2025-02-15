from django import forms
from .models import Hesap

class HesapAcForm(forms.ModelForm):
    class Meta:
        model = Hesap
        fields = ['hesap_turu', 'tel','bakiye']

    hesap_turu = forms.ChoiceField(choices=Hesap.HESAP_TURLERI, label="Hesap Türü")
    bakiye = forms.DecimalField(max_digits=10, decimal_places=2,label="Bakiye")
    tel = forms.CharField(max_length=11, label="Telefon Numarası")

    # __init__ metodunu özelleştiriyoruz
    def __init__(self, *args, **kwargs):
        # Giriş yapan kullanıcıyı kwargs'dan alıyoruz
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        hesap = super().save(commit=False)
        if self.user:
            hesap.musteri = self.user  # Hesap, doğru kullanıcıya bağlanmalı
        if commit:
            hesap.save()
        return hesap

from django import forms
from .models import ParaGonderme, Hesap
from django.contrib.auth import get_user_model
User = get_user_model()
class ParaGonderForm(forms.ModelForm):
    class Meta:
        model = ParaGonderme
        fields = ['gonderen', 'alici_iban', 'miktar']

    gonderen = forms.ModelChoiceField(queryset=Hesap.objects.filter(), empty_label="Hesap Seçin")
    alici_iban = forms.CharField(max_length=26, label="Alıcı IBAN")
    miktar = forms.DecimalField(max_digits=10, decimal_places=2, label="Gönderilecek Miktar")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Kullanıcıyı alıyoruz
        super().__init__(*args, **kwargs)
        if user:
            # Kullanıcının hesaplarını filtreliyoruz
            self.fields['gonderen'].queryset = Hesap.objects.filter(musteri=user)  # Sadece giriş yapan kişinin hesapları gösterilecek

    def clean_miktar(self):
        miktar = self.cleaned_data.get('miktar')
        gonderen_hesap = self.cleaned_data.get('gonderen')

        if miktar > gonderen_hesap.bakiye:
            raise forms.ValidationError("Yetersiz bakiye!")
        return miktar

    