import random
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

import random
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_hesap_no():
    """16 haneli rastgele bir hesap numarası oluştur."""
    return "".join([str(random.randint(0, 9)) for _ in range(16)])

def generate_iban():
    """Rastgele bir IBAN oluştur ve hesap numarasını içine yerleştir."""
    country_code = "TR"  # Türkiye için ülke kodu
    bank_code = "00062"  # Örnek banka kodu
    hesap_no = generate_hesap_no()  # Hesap numarası üret
    checksum = "00"  # Kontrol numarası (daha gelişmiş kurallar eklenebilir)
    iban = f"{country_code}{checksum}{bank_code}{hesap_no}"
    return iban, hesap_no  # IBAN ve hesap numarasını birlikte döndür


from django.db import models
from django.contrib.auth.models import User

# IBAN oluşturmak için fonksiyon (örnek)
import random
import string

def generate_iban():
    """IBAN numarasını otomatik oluşturmak için bir fonksiyon."""
    iban = 'TR' + ''.join(random.choices(string.digits, k=24))  # Türkiye için örnek IBAN formatı
    hesap_no = ''.join(random.choices(string.digits, k=16))  # Hesap numarası
    return iban, hesap_no

class Hesap(models.Model):
    """Hesap modeli."""
    HESAP_TURLERI = [
        ('vadesiz', 'Vadesiz Hesap'),
        ('vadeli', 'Vadeli Hesap'),
        ('yatirim', 'Yatırım Hesabı'),
    ]

    musteri = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hesaplar")
    hesap_no = models.CharField(max_length=16, unique=True, editable=False)  # IBAN'dan türetilir
    iban = models.CharField(max_length=26, unique=True, editable=False)  # Otomatik atanır
    hesap_turu = models.CharField(max_length=10, choices=HESAP_TURLERI)
    bakiye = models.DecimalField(max_digits=10, decimal_places=2)  # Bakiye elle girilecek
    acilis_tarihi = models.DateTimeField(auto_now_add=True, editable=False)
    tel = models.CharField(max_length=11)

    def save(self, *args, **kwargs):
        """Hesap oluşturulmadan önce otomatik değerleri doldur."""
        if not self.iban:  # Eğer IBAN atanmadıysa
            self.iban, self.hesap_no = generate_iban()  # IBAN ve hesap numarasını oluştur
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hesap_no} - {self.hesap_turu} - {self.musteri.username} - {self.bakiye} TL"

    

class ParaGonderme(models.Model):
    gonderen = models.ForeignKey(Hesap, related_name="gonderen", on_delete=models.CASCADE)
    alici_iban = models.CharField(max_length=34)
    miktar = models.DecimalField(max_digits=10, decimal_places=2)
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gonderen} -> {self.alici_iban} - {self.miktar} TL"
    
from django.utils import timezone

class Islem(models.Model):
    """Para gönderme ve çekme işlemlerinin kaydedildiği model"""
    GONDERME = 'Gonderme'
    CEKME = 'Cekme'
    ISLEM_TIPI = [
        (GONDERME, 'Para Gönderme'),
        (CEKME, 'Para Çekme'),
    ]
    
    gonderen = models.ForeignKey(Hesap, related_name='gonderilen_islemler', on_delete=models.CASCADE)
    alici = models.ForeignKey(Hesap, related_name='alınan_islemler', on_delete=models.CASCADE)
    miktar = models.DecimalField(max_digits=10, decimal_places=2)
    islem_tipi = models.CharField(max_length=10, choices=ISLEM_TIPI)
    tarih_ve_saat = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.gonderen} -> {self.alici} : {self.miktar} TL ({self.islem_tipi})"
    
class CurrencyData(models.Model):
    currency_type = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency_type}: {self.value}"

class CurrencyDatakripto(models.Model):
    currency_type = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency_type}: {self.value}"