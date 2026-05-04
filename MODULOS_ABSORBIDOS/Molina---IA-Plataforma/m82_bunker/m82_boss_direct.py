import requests
import time

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
BUNKER_BRENT = 125.5 

def motor_agi_boss(texto):
    t = texto.lower()
    # Lógica de procesamiento de noticias LSEG / Reuters
    if any(word in t for word in ["crude", "inventory", "api", "gasoline", "stockpiles"]):
        impacto = "🚨 BULLISH (ALCISTA)" if any(w in t for w in ["fell", "fall", "draw", "down", "-"]) else "⚖️ NEUTRAL"
        return (f"🏛️ M82 AGI INSIGHT:\n\n"
                f"📊 Inteligencia: Detectado reporte de inventarios.\n"
                f"🛡️ Sentimiento: {impacto}.\n\n"
                f"💡 JUICIO: El Brent en el búnker ($125.5) mantiene prima de soberanía. "
                "Los datos de LSEG validan nuestra tesis de escasez. Ejecución firme.")
    
    elif any(word in t for word in ["natgas", "expand", "lng", "gas"]):
        return ("🔥 M82 AGI INSIGHT:\n\nConfirmación de expansión en Natural Gas. "
                "El Capex de $2.85B de Expand Energy asegura la viabilidad de la Serie 2028. "
                "Soberanía energética absoluta.")
    
    return "🧠 M82: Data recibida, Boss. Procesando impacto en la arquitectura principal..."

def iniciar_puente():
    last_id = 0
    print("--- SISTEMA LIMPIO: M82 AGI EN ESCUCHA ---")
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id + 1}", timeout=10).json()
            for u in r.get("result", []):
                last_id = u["update_id"]
                if "message" in u and "text" in u["message"]:
                    msg_boss = u["message"]["text"]
                    cid = u["message"]["chat"]["id"]
                    
                    # Respuesta inmediata de la AGI
                    analisis = motor_agi_boss(msg_boss)
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": cid, "text": analisis})
        except Exception:
            pass
        time.sleep(1)

if __name__ == '__main__':
    iniciar_puente()
