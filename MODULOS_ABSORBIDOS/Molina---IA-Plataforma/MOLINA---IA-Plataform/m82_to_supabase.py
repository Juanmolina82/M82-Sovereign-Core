import os
from supabase import create_client, Client
import hashlib
import datetime

# --- CONFIGURACIÓN DE SEGURIDAD M82 ---
URL = "TU_PROYECTO_URL.supabase.co"
KEY = "TU_API_KEY_ANON"
supabase: Client = create_client(URL, KEY)

def ingest_strategic_news(title, risk, impact):
    # Generamos la data bajo el protocolo Apache-2.0
    data = {
        "title": title,
        "risk_level": risk,
        "impact_sector": impact,
        "timestamp": str(datetime.datetime.now()),
        "protocol": "M82-QUANTUM-V1"
    }
    
    # Firma Digital para validación en la App
    sig = hashlib.sha256(str(data).encode()).hexdigest()[:12].upper()
    data["digital_sig"] = sig

    try:
        # Enviamos a la tabla 'news_feed' (debes crearla en Supabase)
        response = supabase.table("news_feed").insert(data).execute()
        print(f"✅ INGESTIÓN EXITOSA | SIG: {sig}")
    except Exception as e:
        print(f"🛑 FALLO DE CONEXIÓN: {e}")

if __name__ == "__main__":
    # Prueba de carga con datos de tu feed
    ingest_strategic_news(
        "Escalada en Odesa: Ataque con drones", 
        "HIGH", 
        "Geopolitical/Supply Chain"
    )
