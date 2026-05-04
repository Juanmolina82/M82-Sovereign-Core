import requests
import time

TOKEN = '8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4'

def m82_brain(text):
    msg = text.lower()
    if any(w in msg for w in ['opec', 'uae', 'cuba', 'trump', 'brent', 'oil', 'inventory']):
        return "🚨 ALERTA M82: IMPACTO CRÍTICO.\n\nAnálisis: Movimiento estratégico detectado.\n\nJuicio: Tesis de $125.5 firme, Chairman."
    return "🧠 M82 ANALYST: Reporte procesado con éxito, Chairman."

def start_bunker():
    last_id = 0
    print("🏛️ M82 TURBO-RESILIENTE: BUSCANDO AL CHAIRMAN...")
    
    while True:
        try:
            # Petición ultra-corta para evitar que la red inestable la aborte
            r = requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates', 
                             params={'offset': last_id + 1, 'timeout': 5}, timeout=10).json()
            
            for u in r.get('result', []):
                last_id = u['update_id']
                if 'message' in u:
                    chat_id = u['message']['chat']['id']
                    res = m82_brain(u['message'].get('text', ''))
                    requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', 
                                  json={'chat_id': chat_id, 'text': res}, timeout=10)
                    print(f"⚡ Enviado al Chairman.")
        except Exception:
            # Si la red falla, el bot espera 0.1s y salta de nuevo al ataque
            time.sleep(0.1)
            continue

if __name__ == "__main__":
    start_bunker()
