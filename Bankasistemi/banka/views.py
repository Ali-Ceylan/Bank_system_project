from django.contrib.auth import get_user_model
user = get_user_model()
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Hesap, Islem, User
from .forms import ParaGonderForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render
import yfinance as yf
from django.http import JsonResponse
from .models import CurrencyData,CurrencyDatakripto
from django.core.mail import send_mail


def piyasa(request):
    data={
    'currency_data' : CurrencyData.objects.all(),
    
    }
    return render(request, 'piyasalar.html', data)


def get_currency_data(request):
    currency_data = CurrencyData.objects.all()
    data = list(currency_data.values())
    return JsonResponse(data, safe=False)






# Form verilerini almak için


def anasayfa(request):
    hesaplar = Hesap.objects.filter(musteri=request.user) if request.user.is_authenticated else []
    data = {
        "hesaplar": hesaplar,
        'currency_data': CurrencyData.objects.all(),
        'currency_data2':CurrencyDatakripto.objects.all(),
    }
    return render(request, "anasayfa.html", data)

def login(request):
    return render(request, "account/login.html")



from .forms import HesapAcForm,ParaGonderForm

def hesapac(request):
    if request.method == 'POST':
        form = HesapAcForm(request.POST, user=request.user)  # Giriş yapan kullanıcıyı formda gönderiyoruz
        if form.is_valid():
            form.save()  # Hesap verilerini kaydediyoruz
            return redirect('anasayfa')  # Başarılı hesap açma sayfasına yönlendirme
    else:
        form = HesapAcForm(user=request.user)

    return render(request, 'hesapac.html', {'form': form})


def hesaplar(request):
    data = {
        
        "hesaplar": Hesap.objects.filter(musteri=request.user),

        }
    return render(request, "hesaplar.html", data)

def kullanıcılar(request):
    data = {
        
        "kullanıcılar": Hesap.objects.all(),

        }
    return render(request, "kullanıcılar.html", data)
def hesapgecmisi(request):
    if not request.user.is_authenticated:
        return redirect('login')
    hesaplar = Hesap.objects.filter(musteri=request.user)
    islemler = Islem.objects.filter(gonderen__in=hesaplar)  # veya gonderen=request.user
    return render(request, 'hesapgecmisi.html', {'islemler': islemler})
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from .models import Hesap, Islem
from .forms import ParaGonderForm
from django.contrib.auth.models import User

def para_gonder(request):
    """Para gönderme işlemi"""
    if request.method == "POST":
        form = ParaGonderForm(request.POST, user=request.user)
        if form.is_valid():
            gonderen = form.cleaned_data['gonderen']
            alici_iban = form.cleaned_data['alici_iban']
            miktar = form.cleaned_data['miktar']

            try:
                # Alıcı hesabını bul
                alici = Hesap.objects.get(iban=alici_iban)

                # Gönderen hesabın bakiyesini kontrol et
                if gonderen.bakiye < miktar:
                    messages.error(request, "Yetersiz bakiye.")
                    return render(request, 'paragonder.html', {'form': form, 'islemler': Islem.objects.filter(gonderen__in=Hesap.objects.filter(musteri=request.user))})
                
                 # Gönderen ve alıcı hesaplarının bakiyelerini güncelle
                gonderen.bakiye -= miktar
                alici.bakiye += miktar

                # Hesapları kaydet
                gonderen.save()
                alici.save()

                # İşlem geçmişini kaydet
                Islem.objects.create(
                    gonderen=gonderen,
                    alici=alici,
                    miktar=miktar,
                    islem_tipi='Gonderme',
                    tarih_ve_saat=timezone.now()
                )

                # Alıcının email adresini User tablosundan çek
                alici_user = User.objects.get(id=alici.musteri.id)
                
                # Gönderenin adını User tablosundan çek
                gonderen_user = User.objects.get(id=gonderen.musteri.id)

                subject = f'Size  {gonderen_user.first_name} {gonderen_user.last_name} tarafından para geldi:'
                message = f'{alici.iban} numaralı Hesabınıza {miktar} TL {gonderen_user.first_name} {gonderen_user.last_name} tarafından para gönderildi.'
                from_email = 'diyetisyendiyet190@gmail.com'  # Use a valid sender email address
                to_email = alici_user.email  # Assuming 'musteri' is a ForeignKey to a User model
                subject2 = f'{alici_user.first_name} {alici_user.last_name} kişisine para gönderdiniz.'
                message2 = f'Hesabınızdan {miktar} TL para  {alici.iban} numaralı ibana gönderildi.'
                to_email2 = gonderen_user.email
                try:
                     send_mail(subject, message, from_email, [to_email])
                     send_mail(subject2, message2, from_email, [to_email2])
                     messages.success(request, f"{miktar} TL başarıyla gönderildi ve alıcısına e-posta gönderildi.")
                except Exception as e:
                    messages.error(request, f'E-posta gönderilirken bir hata oluştu: {e}')

                # Formu temizle ve başarılı mesaj ver
                form = ParaGonderForm(user=request.user)  # Yeni boş form oluştur
                
                return render(request, 'paragonder.html', {'form': form, 'islemler': Islem.objects.filter(gonderen__in=Hesap.objects.filter(musteri=request.user))})

            except Hesap.DoesNotExist:
                 messages.error(request, "Alıcı IBAN bulunamadı.")
                 return render(request, 'paragonder.html', {'form': form, 'islemler': Islem.objects.filter(gonderen__in=Hesap.objects.filter(musteri=request.user))})
            except Exception as e:
                messages.error(request, f"Para gönderilirken bir hata oluştu: {e}")
                return render(request, 'paragonder.html', {'form': form, 'islemler': Islem.objects.filter(gonderen__in=Hesap.objects.filter(musteri=request.user))})
    else:
        form = ParaGonderForm(user=request.user)
        
    hesaplar = Hesap.objects.filter()  # Kullanıcının hesapları
    islemler = Islem.objects.filter(gonderen__in=hesaplar)
    return render(request, 'paragonder.html', {'form': form, 'islemler': islemler})

from django.contrib.auth import  logout
def logout_(request):
    logout(request)
    return redirect("anasayfa")