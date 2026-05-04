import requests
import time

# Configuración de Seguridad Molina Holdings
TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def ejecutar_centinela():
    # 1. Parámetros de la Realidad LSEG (Noticia 30/04/2026)
    brent_actual = 125.0
    bono_10y = 4.43
    
    # 2. Lógica de Estrés Louisiana-Flow
    ebitda_base = 5000000
    deuda_total = 15000000
    
    # Impacto: -12% EBITDA por costos energía + aumento de tasas
    ebitda_ajustado = ebitda_base * 0.88
    interes_extra = deuda_total * (0.0050) # +50 bps
    fcf_final = ebitda_ajustado - interes_extra
    
    # 3. Construcción del Mensaje (Sintaxis Limpia)
    lineas = [
        "🏛️ M82 | REPORTE SOBERANO",
        "--------------------------",
        f"📍 BRENT: ${brent_actual} (MAX 4 AÑOS)",
        f"📍 BONO 10Y: {bono_10y}% (HAWKISH)",
        "--------------------------",
        "📊 PROYECCION LOUISIANA:",
        f"💰 FCF ESTIMADO: ${fcf_final:,.2f}",
        "🛡️ STATUS: CONEXION SEGURA",
        "--------------------------",
        "EL CENTINELA NO DUERME."
    ]
    mensaje = "\n".join(lineas)
    
    # 4. Envío de Ignición
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": mensaje})
        if r.status_code == 200:
            print("✅ Transmisión exitosa al Chairman.")
        else:
            print(f"❌ Error de Servidor: {r.text}")
    except Exception as e:
        print(f"🛑 Fallo de Red: {e}")

if __name__ == "__main__":
    print("🚀 M82 Sovereign Bot Iniciado...")
    ejecutar_centinela()
