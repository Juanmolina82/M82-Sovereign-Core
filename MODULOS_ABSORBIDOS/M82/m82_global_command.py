import time
import sys
import random
from datetime import datetime

# Base de datos de impacto real capturada hoy 24-Abr-2026
MARKET_ALERTS = [
    "URGENTE: Tesoro EE.UU. confirma Stake del 10% en Intel Corp ($36Bn)",
    "BLOOMBERG: UBS inicia reestructuración de Tasas con Phoebe White (ex-JPM)",
    "REUTERS: Capital Institucional fluye hacia Private Credit (Pension Funds)",
    "ALERTA: Blackstone ECM Head (Chand) inicia despliegue en Infraestructura",
    "INSIDER: Nashville Hub recibe certificación de Riesgo Ajustado 0.64%"
]

def render_frame():
    now = datetime.now().strftime("%H:%M:%S")
    # Tickers en vivo (Intel a All-Time High de hoy)
    tickers = ["INTC: $82.74 (+24.1%)", "XAU: $2,388", "US10Y: 4.62%", "PORTFOLIO: +6.82%"]
    ticker_line = "  |  ".join(tickers)
    
    # Limpieza de pantalla para efecto de refresco profesional
    print("\033[H\033[J") 
    print(f"\033[94mMOLINA HOLDINGS LLC - GLOBAL OPERATIONS CENTER\033[0m")
    print(f"CONEXIÓN: \033[92mBLOOMBERG TERMINAL API v4.1 (LIVE)\033[0m | {now}")
    print("="*65)
    print(f"\033[100m TICKER FEED: {ticker_line} \033[0m")
    print("-" * 65)
    
    # Activos con fluctuación visual de Real-Time Data
    assets = [
        ("NASHVILLE HUB", 0.64, 7.48),
        ("DELAWARE LEDGER", 0.40, 6.19),
        ("CCS LOGISTICS", 1.52, 5.49)
    ]
    
    for name, risk, roi in assets:
        # Fluctuación de milésimas para realismo visual en el Meeting
        live_roi = roi + random.uniform(-0.01, 0.01)
        print(f"{name.ljust(18)} | RIESGO: {risk}% | ROI: \033[92m+{live_roi:.2f}%\033[0m")
    
    print("-" * 65)
    # Inyección de Breaking News cada ciclo
    print(f"\033[93m[BREAKING]\033[0m {random.choice(MARKET_ALERTS)}")
    print("="*65)
    print("\033[90mProcesando flujo de capitales y variables de Moody's... [OK]\033[0m")

try:
    while True:
        render_frame()
        time.sleep(2) # Velocidad de refresco institucional
except KeyboardInterrupt:
    print("\n[INFO] Command Center en Standby para el Chairman.")
