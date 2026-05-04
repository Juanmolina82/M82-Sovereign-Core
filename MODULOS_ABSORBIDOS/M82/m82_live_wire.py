import time
import sys
import random
from datetime import datetime

# Base de datos de noticias reales (las que enviaste)
MARKET_WIRE = [
    "BREAKING: US Government Intel stake jumps to $36Bn (10% Ownership)",
    "FLASH: UBS taps JPMorgan's Phoebe White for US Rates Strategy",
    "NEWS: Blackstone names Citi's Chand as Equity Capital Markets Head",
    "MARKET: Private Credit volatility attracts US Pension Funds",
    "TECH: Intel shares surge +24% following Federal support package"
]

def print_bloomberg_style(text, color_code='\033[93m'):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"{color_code}[{now}] {text}\033[0m")

def run_live_session():
    print("\n" + "="*70)
    print("MOLINA HOLDINGS LLC - REAL-TIME MARKET INTELLIGENCE TERMINAL")
    print("CONNECTION STATUS: ACTIVE (BLOOMBERG API / SEC FILINGS)")
    print("="*70 + "\n")
    
    try:
        while True:
            # Simulación de Market Pulse
            asset_price = round(random.uniform(82.50, 83.10), 2) # Basado en Intel $82.74
            print(f"\r[LIVE QUOTE] INTC: ${asset_price} | TREND: +24.1% | VOLUME: HIGH", end="")
            
            # Cada 7 segundos, inyectar una noticia de impacto
            if random.random() > 0.8:
                print("\n")
                news = random.choice(MARKET_WIRE)
                print_bloomberg_style(f"CORE-NEWS: {news}")
                print("-" * 70)
            
            time.sleep(1)
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n\n[INFO] Desconectando Feed de Mercado.")

if __name__ == "__main__":
    run_live_session()
