import yfinance as yf
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from .models import CurrencyData,CurrencyDatakripto
import math
import pandas as pd


def fetch_and_update_currency_data():
    
    currencies = {
    'Dolar':'USDTRY=X',
    'Euro':'EURTRY=X',
    'BIST100': 'XU100.IS',
    'Euro/Dolar':'EURUSD=X',
    'İngiliz Sterlini':'GBPTRY=X',
    'Bitcoin/USD':'BTC-USD',
    'Altın/USD': 'GC=F', # Altın
    'Gümüş/USD':'SI=F',  # Gümüş
    'PETROL':'CL=F',
    }
    for currency_type , ticker in currencies.items():
        try:
            data = yf.download(tickers = ticker, period="1d",progress=False)
            if not data.empty:
                last_price = data["Close"].iloc[-1]
                print(f"{currency_type} için alınan veri: {last_price} ({type(last_price)})")

                if isinstance(last_price, pd.Series):
                     if not last_price.empty:
                         try:
                             value = Decimal(str(last_price.iloc[0]))
                             update_or_create_data(
                                 currency_type = currency_type, 
                                 value = value
                             )
                         except InvalidOperation as e:
                             print(f"{currency_type} için ondalıklı sayıya çevrilemedi(Series): {last_price} - hata: {e}")
                     else:
                       print(f"{currency_type} için pandas.Series boş: {last_price}")
                elif isinstance(last_price,(int, float)) and not math.isnan(last_price):
                    try:
                         value = Decimal(str(last_price))
                         update_or_create_data(
                            currency_type = currency_type, 
                            value = value
                         )
                    except InvalidOperation as e:
                        print(f"{currency_type} için ondalıklı sayıya çevrilemedi: {last_price} - hata: {e}")
                else:
                    print(f"{currency_type} için geçersiz veri: {last_price}")
            else:
                print(f"{currency_type} için veri alınamadı!")
        except Exception as e:
            print(f"yfinance hatası: {currency_type} - {e}")


def update_or_create_data(currency_type, value):
    CurrencyData.objects.update_or_create(
        currency_type=currency_type,
        defaults={'value': value, 'timestamp': timezone.now()}
    )




