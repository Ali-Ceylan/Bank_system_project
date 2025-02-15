from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.anasayfa, name="anasayfa"),
    path("anasayfa", views.anasayfa, name="anasayfa"),
    path("hesapac", views.hesapac, name="hesapac"),
    path("hesaplar", views.hesaplar, name="hesaplar"),
    path("paragonder", views.para_gonder, name="paragonder"),
    path("hesapgecmisi", views.hesapgecmisi, name="hesapgecmisi"),
    path("piyasalar", views.piyasa, name="piyasalar"),
    path('piyasalar/', views.piyasa, name='piyasa_verileri'),
    path('piyasa_verileri/', views.piyasa, name='piyasa_verileri_data'),
    path('get_currency_data/', views.get_currency_data, name='get_currency_data'),
    path("kullanıcılar", views.kullanıcılar, name="kullanıcılar"),
]
