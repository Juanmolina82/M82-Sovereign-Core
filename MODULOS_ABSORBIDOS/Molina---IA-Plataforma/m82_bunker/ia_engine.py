import time
import random
from datetime import datetime

# Códigos de color para emular la pantalla de Bloomberg
GOLD = '\033[93m'
WHITE = '\033[97m'
RED = '\033[91m'
RESET = '\033[0m'

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def main():
    print(f"\n{GOLD}" + "="*95)
    print(f"{'MOLINA HOLDINGS LLC | ESTRATEGIA SOBERANA M82':^95}")
    print(f"{'US INDEX UPDATE | BRENT MONITORING | INSTITUTIONAL PRESTIGE':^95}")
    print("="*95 + f"{RESET}\n")
    
    while True:
        # Estructura estilo Bloomberg
        market_data = [
            f"{GOLD}DOW JONES   {WHITE} 49,374.09   {RED}▼ 73.34   (0.15%){RESET}",
            f"{GOLD}S&P 500     {WHITE}  7,099.85   {RED}▼ 26.21   (0.37%){RESET}",
            f"{GOLD}NASDAQ      {WHITE} 24,317.04   {RED}▼ 151.44  (0.62%){RESET}",
            f"{WHITE}[{get_timestamp()}] {GOLD}ALERTA:{WHITE} Flujo en Ormuz estable. Arbitraje activo.{RESET}",
            f"{WHITE}[{get_timestamp()}] {GOLD}SENTIMENT:{WHITE} 'HIGHLY UNLIKELY' - Dominancia confirmada.{RESET}"
        ]
        
        # Imprimir una línea a la vez para el efecto "Smooth Scroll"
        print(random.choice(market_data))
        
        # Pausa para legibilidad en OBS
        time.sleep(1.2)

if __name__ == "__main__":
    main()
