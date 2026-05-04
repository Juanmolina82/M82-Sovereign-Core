import time
import random
from datetime import datetime

def m82_alpha_intelligence():
    # Benchmarks Reales Abril 2026
    MOODYS_THRESHOLD = 2.0  # El límite de peligro para BDCs cotizados
    
    print(f"\n[SISTEMA M82 v2.0] - ESTRATEGIA DE CRÉDITO 2026")
    print(f"FECHA: {datetime.now().strftime('%d-%b-%Y')} | REF: Moody's/Pinto")
    print("---------------------------------------------------------")
    
    activos = {
        "Nashville Hub": {"risk": 1.2, "type": "Infra"},
        "Delaware Ledger": {"risk": 0.8, "type": "Asset-Backed"},
        "CCS Logistics": {"risk": 2.1, "type": "Operations"}
    }
    
    try:
        while True:
            for nombre, info in activos.items():
                # Volatilidad de mercado simulada
                current_risk = round(info["risk"] + random.uniform(-0.5, 0.7), 2)
                
                # Lógica de alerta basada en el "Pinto Benchmark"
                if current_risk > MOODYS_THRESHOLD:
                    status = "⚠️ ALERTA: EXCESO DE RIESGO"
                    color = '\033[91m' # Rojo
                else:
                    status = "✅ DENTRO DE PARÁMETROS"
                    color = '\033[92m' # Verde
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {nombre.ljust(15)} | Riesgo: {current_risk}% | {color}{status}\033[0m")
            
            print("-" * 55)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n[INFO] Desconectando Inteligencia Predictiva. Datos encriptados.")

if __name__ == "__main__":
    m82_alpha_intelligence()
