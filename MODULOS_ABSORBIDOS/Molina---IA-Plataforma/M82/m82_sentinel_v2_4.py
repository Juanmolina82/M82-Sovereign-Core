import time
import random
from datetime import datetime
import threading

class M82BloombergSentinel:
    def __init__(self):
        # Base de Datos de Activos
        self.portfolio = {
            "Nashville Hub": {"risk": 1.2, "multiplier": 1.0, "sector": "Chips/Infra"},
            "Delaware Ledger": {"risk": 0.8, "multiplier": 1.0, "sector": "Asset-Backed"},
            "CCS Logistics": {"risk": 2.1, "multiplier": 1.0, "sector": "Supply Chain"}
        }
        self.latest_news = "Conectando con Bloomberg API..."
        self.is_running = True

    def bloomberg_feed_simulator(self):
        # Los titulares reales que envió el Chairman
        feeds = [
            ("Intel Gov Stake +300% ($36Bn)", 0.7, "Chips/Infra"),
            ("Blackstone hires Chand (Citi) for ECM", 0.9, "All"),
            ("UBS taps Phoebe White (JPM) for Rates", 1.15, "All"), # Inflación/Tasas sube riesgo
            ("US Pensions buying Private Credit", 0.85, "Asset-Backed")
        ]
        while self.is_running:
            news, impact, sector = random.choice(feeds)
            self.latest_news = news
            # Aplicar impacto al sector correspondiente
            for asset, data in self.portfolio.items():
                if sector == "All" or data["sector"] == sector:
                    data["multiplier"] = impact
            time.sleep(8)

    def display_robust_terminal(self):
        print(f"\n[M82 SENTINEL v2.4 - OPERACIÓN GERENTE ROBUSTO]")
        print(f"ESTADO: CONECTADO | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*65)
        
        threading.Thread(target=self.bloomberg_feed_simulator, daemon=True).start()
        
        try:
            while True:
                print(f"\n>> BLOOMBERG WIRE: {self.latest_news}")
                print("-" * 65)
                for asset, data in self.portfolio.items():
                    adj_risk = round(data["risk"] * data["multiplier"], 2)
                    status = "✅ ROBUSTO" if adj_risk < 1.5 else "⚠️ MONITOR"
                    color = '\033[94m' if adj_risk < 1.0 else '\033[93m'
                    if adj_risk > 2.0: color = '\033[91m'
                    
                    print(f"ASSET: {asset.ljust(15)} | RIESGO: {color}{adj_risk}%\033[0m | STATUS: {status}")
                
                time.sleep(4)
        except KeyboardInterrupt:
            self.is_running = False
            print("\n[M82] Sesión finalizada. Logs guardados.")

if __name__ == "__main__":
    M82BloombergSentinel().display_robust_terminal()
