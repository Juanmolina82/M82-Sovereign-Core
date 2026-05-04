import requests
import time

TOKEN = '8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4'

def m82_brain(text):
    msg = text.lower()
    if any(w in msg for w in ['opec', 'uae', 'cuba', 'trump', 'oil', 'brent']):
        return "🚨 ALERTA M82: IMPACTO CRÍTICO.\n\nJuicio: Tesis de $125.5 firme, Chairman."
    return "🧠 M82: Recibido sin demora, Chairman."

def start_bunker():
    last_id = 0
    # Simulamos un navegador real para saltar el firewall del router
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    print("🛡️ M82 BYPASS ACTIVADO (Saltando Firewall)...")
    
    while True:
        try:
            # Timeout corto para evitar que el firewall cierre la conexión por inactividad
            url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
            r = s.get(url, params={'offset': last_id + 1, 'timeout': 2}, timeout=5).json()
            
            if r.get('result'):
                for u in r['result']:
                    last_id = u['update_id']
                    if 'message' in u:
                        chat_id = u['message']['chat']['id']
                        txt = u['message'].get('text', '')
                        res = m82_brain(txt)
                        # Respuesta directa
                        s.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', 
                               json={'chat_id': chat_id, 'text': res}, timeout=5)
                        print("⚡ Bypass exitoso: Mensaje entregado.")
        except:
            time.sleep(0.1) # Reintento agresivo

if __name__ == "__main__":
    start_bunker()
