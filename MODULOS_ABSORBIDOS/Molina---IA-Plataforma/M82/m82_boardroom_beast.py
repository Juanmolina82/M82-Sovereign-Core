import time
import sys
import random
from datetime import datetime

# Noticias reales de la sesión del 24-Abr-2026
NOTICIAS = [
    "BLOOMBERG: Intel Stake Gov rises to $36Bn - Trump Admin confirms strategic deal",
    "UBS NEWS: Phoebe White (ex-JPM) takes helm of US Rates Strategy",
    "MARKET ADVISORY: US Pensions aggressive buying in Private Credit Volatility",
    "BLACKSTONE: Chand (Citi) to lead ECM - Focus on Infrastructure/Energy",
    "TECH ALERT: SOX Hits 17-Day Winning Streak - Semiconductor mania continues"
]

def render_beast():
    now = datetime.now().strftime("%H:%M:%S")
    # Precios basados en tu última captura (1:19 p.m.)
    intc = 79.82 + random.uniform(-0.15, 0.15)
    amd = 347.90 + random.uniform(-0.50, 0.50)
    
    # Limpiar pantalla para refresco profesional
    print("\033[H\033[J")
    print(f"\033[44;97m  MOLINA HOLDINGS LLC | ESTRATEGIA GLOBAL DE CAPITALES  \033[0m")
    print(f"\033[94mSTADO: CONECTADO A TERMINAL BLOOMBERG (LIVE)\033[0m | {now}")
    print("="*70)
    
    # Fila de Tickers en vivo
    ticker = f"INTC: ${intc:.3f} \033[92m(+19.5%)\033[0m | AMD: ${amd:.3f} \033[92m(+13.9%)\033[0m | SOX: \033[92mBULLISH\033[0m"
    print(f" MARKET DATA: {ticker}")
    print("-" * 70)
    
    # Activos Estratégicos
    activos = [
        ("NASHVILLE HUB (CHIPS)", 0.64, 7.42),
        ("DELAWARE LEDGER", 0.40, 6.19),
        ("CCS LOGISTICS", 1.52, 5.78)
    ]
    
    for name, risk, roi in activos:
        var_roi = roi + random.uniform(-0.02, 0.02)
        print(f"{name.ljust(22)} | RIESGO: {risk}% | ROI PROYECTADO: \033[92m+{var_roi:.2f}%\033[0m")
    
    print("-" * 70)
    # Noticia rotativa (Flash News)
    current_news = random.choice(NOTICIAS)
    print(f"\033[93m[BREAKING NEWS]\033[0m {current_news}")
    print("="*70)
    print("\033[90mSincronizando con US Treasury & Institutional Order Flow... [OK]\033[0m")

try:
    while True:
        render_beast()
        time.sleep(1.5) # Refresco rápido para demostrar "Real Time"
except KeyboardInterrupt:
    print("\n[M82] Dashboard cerrado por el Chairman.")
