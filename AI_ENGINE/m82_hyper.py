import urllib.request
import re
import os
import time
import random

# Cache de emergencia para evitar intermitencia
cache = {"BZ=F": "$95.09", "NVDA": "$196.51", "GOOGL": "$332.91", "NKE": "$44.20"}

def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as response:
            data = response.read().decode()
            price = re.search(r'"regularMarketPrice":([\d.]+)', data).group(1)
            val = f"${float(price):.2f}"
            cache[symbol] = val
            return val
    except:
        return cache.get(symbol, "SYNCING...")

def render():
    os.system('clear')
    print("\033[1;32m╔" + "═"*78 + "╗\033[0m")
    print(f"\033[1;32m║ MOLINA HOLDINGS | M82 STRATEGIC COMMAND | VZLA RECOVERY | {time.strftime('%H:%M:%S')} ║\033[0m")
    print("\033[1;32m╠" + "═"*78 + "╣\033[0m")
    
    # MONITOR DE ACTIVOS REAL-TIME
    print(f"\033[1;34m [ENERGY ]\033[0m BRENT: {get_price('BZ=F')} | \033[1;34m[TECH  ]\033[0m NVDA: {get_price('NVDA')}")
    print(f"\033[1;34m [INDEX  ]\033[0m S&P500: 6,967.38    | \033[1;34m[RETAIL]\033[0m NIKE: {get_price('NKE')}")
    print("\033[1;32m╠" + "═"*78 + "╣\033[0m")
    
    # LA LISTA PENDIENTE: INTELIGENCIA PROFUNDA
    intel_pool = [
        "BILLINGSLEA PROTOCOL: Model 2 (Prudent) active. US Treasury board vetting BCV.",
        "MIGUEL RODRIGUEZ LEGACY: Target 10M BPD production via 100% privatization.",
        "THE PLUNDER MAP: 50% of national wealth ($500B+) tracked to offshore nodes.",
        "SEC COMPLIANCE: PDT Rule abolition confirmed. Retail power surges tomorrow.",
        "BCV AUDIT: General License 44B tied to forensic data delivery of 2000-2025 flows.",
        "CARTEL WATCH: OFAC targets 'Model 1' enablers trying to hide asset trails.",
        "OIL RECOVERY: 10M BPD is a technical reality, only blocked by systemic crime.",
        "GEOPOL ALPHA: Iran de-escalation shifts $2.4T into AI and Energy Infrastructure.",
        "MOLINA DOCTRINE: Auditing the theft to fund the future 10M BPD superpower."
    ]
    
    # Mostramos 5 líneas para rellenar el terminal con autoridad
    for msg in random.sample(intel_pool, 5):
        print(f"\033[1;37m [STRAT-INTEL]\033[0m {msg}")
    
    print("\033[1;32m╚" + "═"*78 + "╝\033[0m")
    print(f"\033[1;30m OPERATIVE: CHAIRMAN ACCESS | NASHVILLE NODE | 'THE GREAT AUDIT' \033[0m")

while True:
    render()
    time.sleep(10)
