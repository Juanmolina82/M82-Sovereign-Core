import time
import requests

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"
HORARIOS = ["05:00", "09:00", "12:00", "16:00", "20:00", "00:00"]

def avisar_chairman():
    while True:
        ahora = time.strftime("%H:%M")
        if ahora in HORARIOS:
            msg = f"🏛️ ESTRATEGIA M82: Chairman, es hora del POST ROBUSTO ({ahora}). Domine el mercado ahora."
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})
            time.sleep(61) # Evita duplicados en el mismo minuto
        time.sleep(30)

if __name__ == "__main__":
    avisar_chairman()
