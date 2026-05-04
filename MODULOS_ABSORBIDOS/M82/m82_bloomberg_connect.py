import time
import random
from datetime import datetime
import threading

# Simulación de API de Bloomberg / News Stream
NEWS_STREAM = [
    "BREAKING: US Govt stake in Intel rises to $36Bn. Sector: Chips/Infra",
    "UBS hires JPMorgan's Phoebe White for US Rates Strategy. Focus: Inflation",
    "Blackstone names Citi's Chand as Equity Capital Markets Head",
    "Private Credit: US Pensions increase allocation to Asset-Backed debt"
]

class M82Terminal:
    def __init__(self):
        self.risk_multiplier = 1.0
        self.last_news = "Esperando feed de Bloomberg..."
        self.active = True

    def news_api_listener(self):
        while self.active:
            # Simula la llegada de una noticia de la API
            self.last_news = random.choice(NEWS_STREAM)
            if "Intel" in self.last_news or "Gov" in self.last_news:
                self.risk_multiplier = 0.75  # Baja el riesgo por respaldo estatal
            elif "Inflation" in self.last_news:
                self.risk_multiplier = 1.10  # Sube el riesgo por presión de tasas
            time.sleep(10)

    def run_monitor(self):
        print(f"\n[M82 TERMINAL v2.3 - BLOOMBERG API INTEGRATION]")
        print(f"ESTADO: GERENTE ROBUSTO ACTIVO | {datetime.now().strftime('%Y-%m-%d')}")
        print("-" * 60)
        
        # Iniciar el hilo de la API
        threading.Thread(target=self.news_api_listener, daemon=True).start()
        
        try:
            while True:
                base_risk = 1.5
                current_risk = round(base_risk * self.risk_multiplier, 2)
                
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] NEWS: {self.last_news}")
                print(f"ADJUSTED PORTFOLIO RISK: {current_risk}%")
                
                # Visualización de Activos
                status = "STABLE" if current_risk < 1.8 else "VOLATILE"
                color = '\033[92m' if status == "STABLE" else '\033[93m'
                print(f"SYSTEM STATUS: {color}{status}\033[0m")
                
                time.sleep(5)
        except KeyboardInterrupt:
            self.active = False
            print("\n[INFO] Desconectando API de Bloomberg. Sesión guardada.")

if __name__ == "__main__":
    terminal = M82Terminal()
    terminal.run_monitor()
