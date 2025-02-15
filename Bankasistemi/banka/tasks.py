from .utils import fetch_and_update_currency_data
import threading
from time import sleep
def start_periodic_data_update():
    def periodic_update():
        while True:
            fetch_and_update_currency_data()
            sleep(10) # Veriyi 60 saniyede bir güncelle
    
    update_thread = threading.Thread(target = periodic_update)
    update_thread.daemon = True # Thread'in ana thread'i ile birlikte kapanmasını sağlar
    update_thread.start()


