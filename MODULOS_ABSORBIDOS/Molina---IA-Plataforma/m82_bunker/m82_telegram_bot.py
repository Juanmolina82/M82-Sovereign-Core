import requests
import json
import time
import os

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"
BUNKER_PATH = os.path.expanduser("~/m82_bunker/m82_audit.json")

def enviar_alerta(data):
    msg = (f"🏛️ M82 SYSTEM UPDATE:\n"
           f"Crudo Brent: ${data['petroleo_brent']}\n"
           f"Estatus: {data['pdi_status']}\n"
           f"Factor: {data['fed_watch']}")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def vigilar():
    ultima_data = None
    print("--- M82 SENTINEL ACTIVE ---")
    while True:
        try:
            with open(BUNKER_PATH, 'r') as f:
                data_actual = json.load(f)
            
            # Solo envía si la información es nueva
            if data_actual != ultima_data:
                enviar_alerta(data_actual)
                ultima_data = data_actual
                print("✅ Cambio detectado y reportado al Chairman.")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(5) # Revisa el búnker cada 5 segundos

if __name__ == '__main__':
    vigilar()
