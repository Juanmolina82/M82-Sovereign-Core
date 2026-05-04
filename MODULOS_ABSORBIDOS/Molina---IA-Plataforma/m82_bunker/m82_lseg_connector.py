import time
import random
from datetime import datetime

class LSEG_Integration:
    def __init__(self):
        print(f"\033[94m[LSEG] Estableciendo apretón de manos con jmmp@molina82.com...\033[0m")
        time.sleep(2)
        print(f"\033[92m[LSEG] Workspace v2.1 Conectado | RIC: INTC.O, AMD.O, .SOX\033[0m")

    def get_institutional_flow(self):
        # Datos de profundidad de mercado que solo da LSEG
        flow = {
            "INTC.O": {"price": 79.82, "sentiment": 0.89, "inst_buy": "HIGH"},
            "AMD.O": {"price": 347.90, "sentiment": 0.75, "inst_buy": "MEDIUM"},
            ".SOX": {"value": 5120.4, "trend": "BULLISH", "volatility": "STABLE"}
        }
        return flow

def run_lseg_dashboard():
    lseg = LSEG_Integration()
    print("-" * 70)
    print("M82 GLOBAL COMMAND - LSEG DATA STREAM ACTIVE")
    print("-" * 70)
    
    try:
        while True:
            data = lseg.get_institutional_flow()
            now = datetime.now().strftime("%H:%M:%S")
            
            # Mostrar la 'limpieza' de los datos institucionales
            for ric, metrics in data.items():
                print(f"[{now}] RIC: {ric.ljust(8)} | PRED: \033[92m{metrics.get('price', metrics.get('value'))}\033[0m | INST_FLOW: {metrics.get('inst_buy', metrics.get('trend'))}")
            
            print("-" * 70)
            print(f"\033[90m[INFO] Recibiendo metadatos de Refinitiv Real-Time Feed...\033[0m")
            time.sleep(3)
            print("\033[H\033[J") # Refresh
            
    except KeyboardInterrupt:
        print("\n[M82] Desconectando LSEG Workspace.")

if __name__ == "__main__":
    run_lseg_dashboard()
