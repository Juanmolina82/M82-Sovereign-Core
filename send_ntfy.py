#!/usr/bin/env python3
import requests, sys, os

NTFY_TOPIC = "tu_topic_m82"  # ⚠️ Pon aquí tu canal de ntfy exacto

def dispatch_alert(title, message, image_path=None):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    headers = {
        "Title": title,
        "Priority": "high",
        "Tags": "chart_with_upwards_trend,oil_drum"
    }
    
    try:
        # Enviar mensaje con texto
        res = requests.post(url, data=message.encode('utf-8'), headers=headers, timeout=10)
        
        # Enviar adjunto (Tarjeta HD) si existe
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                requests.put(url, data=f, headers={"Filename": os.path.basename(image_path)}, timeout=15)
                
        print(f"📲 Alerta ntfy enviada con éxito (Status {res.status_code})")
    except Exception as e:
        print(f"⚠️ Error al enviar notificación ntfy: {e}")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Nueva tarjeta M82 procesada."
    img = sys.argv[2] if len(sys.argv) > 2 else None
    dispatch_alert("M82 ALERT :: MACRO & OIL", msg, img)
