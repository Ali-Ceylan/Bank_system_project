from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Hesap,Islem,CurrencyData,CurrencyDatakripto



@admin.register(CurrencyData)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("currency_type", "value", "timestamp")
    readonly_fields = ("currency_type", "value", "timestamp")  # Otomatik alanlar sadece okunabilir
    fields = ("currency_type", "value", "timestamp") 

@admin.register(Hesap)
class HesapAdmin(admin.ModelAdmin):
    list_display = ("musteri", "hesap_no", "iban", "hesap_turu", "bakiye", "acilis_tarihi", "tel")
    readonly_fields = ("hesap_no", "iban", "acilis_tarihi")  # Otomatik alanlar sadece okunabilir
    fields = ("musteri", "hesap_turu", "tel", "bakiye")  # Bakiye de dahil edilmiştir, düzenlenebilir

    # Eğer bakiye alanını bazı durumlarda yalnızca okunabilir yapmak istiyorsanız, bunu metodla yapabilirsiniz:
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Eğer bir obje düzenleniyorsa, bakiye okunabilir olabilir
            return self.readonly_fields + ('bakiye',)  # Bakiye sadece okunabilir
        return self.readonly_fields
    
@admin.register(Islem)
class IslemAdmin(admin.ModelAdmin):
    list_display = ("gonderen", "alici", "miktar", "islem_tipi", "tarih_ve_saat")
    list_filter = ("islem_tipi", "tarih_ve_saat")
    search_fields = ("gonderen__hesap_no", "alici__hesap_no", "gonderen__musteri__username", "alici__musteri__username")
    ordering = ("-tarih_ve_saat",)  # Son yapılan işlemi önce gösterir





