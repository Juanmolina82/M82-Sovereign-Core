import requests
import json
import time
import os
from bs4 import BeautifulSoup

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"
BUNKER_PATH = os.path.expanduser("~/m82_bunker/m82_audit.json")
NEWS_URL = "https://www.reuters.com/markets/commodities/"

def enviar_mando(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def analizar_noticias():
    try:
        r = requests.get(NEWS_URL, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text().lower()
        if "brent" in text or "fed" in text or "warsh" in text:
            return "🔥 ALERTA NOTICIAS: Movimiento detectado en Reuters sobre Brent/FED."
        return "⚖️ SENTIMIENTO: Mercados globales estables."
    except:
        return "📡 STATUS: Error de enlace con Reuters."

def ejecutar_agi():
    ultima_data = None
    print("--- M82 AGI CORE INITIALIZED ---")
    while True:
        try:
            # 1. Monitoreo de Búnker
            with open(BUNKER_PATH, 'r') as f:
                data = json.load(f)
            
            # 2. Lógica de Juicio Crítico
            if data != ultima_data:
                noticia = analizar_noticias()
                brent = data.get('petroleo_brent', 0)
                status = data.get('pdi_status', '')
                
                msg = (f"🏛️ M82 AGI REPORT:\n\n"
                       f"📊 Brent: ${brent}\n"
                       f"🌍 Noticia: {noticia}\n"
                       f"🛡️ Estatus: {status}\n\n"
                       f"💡 ACCIÓN RECOMENDADA: Mantener protocolo de soberanía.")
                
                enviar_mando(msg)
                ultima_data = data
                print("✅ Inteligencia enviada al Boss.")
                
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(15) # Ciclo de pensamiento cada 15 segundos

if __name__ == '__main__':
    ejecutar_agi()
