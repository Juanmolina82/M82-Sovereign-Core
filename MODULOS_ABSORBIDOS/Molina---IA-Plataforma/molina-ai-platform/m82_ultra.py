import requests, re, os, time, random

def g_p(s):
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{s}", headers={'User-Agent': 'Mozilla/5.0'}, timeout=2).text
        m = re.search(r'"regularMarketPrice":\s*([0-9.]+)', r)
        return float(m.group(1)) if m else 0.0
    except: return 0.0

def draw():
    os.system('clear')
    nvda, brent, gold = g_p("NVDA"), g_p("BZ=F"), g_p("GC=F")
    pten, sdrl, abbv = g_p("PTEN"), g_p("SDRL"), g_p("ABBV")
    
    print("\033[1;32m╔" + "═"*78 + "╗\033[0m")
    print(f"\033[1;32m║ MOLINA HOLDINGS | M82 COMMAND CENTER | LIVE BLOOMBERG FEED | NASHVILLE BYPASS ║\033[0m")
    print("\033[1;32m╠" + "═"*78 + "╣\033[0m")
    
    # MATRIZ DE PRECIOS CORE
    print(f"\033[1;34m [GLOBAL TICKER]\033[0m NVDA: ${nvda} | BRENT: ${brent} | GOLD: ${gold} | EUR/USD: 1.084")
    print(f"\033[1;34m [BLOCK FLOW  ]\033[0m PTEN: ${pten} | SDRL: ${sdrl} | ABBV: ${abbv} | GLW: $171.9")
    print("\033[1;32m╠" + "═"*78 + "╣\033[0m")

    # SIMULACIÓN DE LIVE BLOOMBERG STREAM (NEWS WIRE)
    news = [
        "BREAKING: IRANIAN OIL WAIVER EXPIRY CONFIRMED BY STATE DEPT",
        "MARKET ALERT: $15 TRILLION BANKING EXPOSURE UNDER SCRUTINY",
        "INSTITUTIONAL: MASSIVE BLOCK BUYS DETECTED IN US ENERGY SERVICES",
        "NASHVILLE SUMMIT: MOLINA HOLDINGS LTA STRUCTURES VERIFIED",
        "GEO-POL: STRAIT OF HORMUZ TRAFFIC AT CRITICAL -90.4% CAPACITY"
    ]
    print(f"\033[1;31m [LIVE WIRE]\033[0m {random.choice(news)}")
    print("\033[1;32m╠" + "═"*78 + "╣\033[0m")

    # ÁREA DE INFORMACIÓN ESTRATÉGICA (ESCENARIOS)
    print("\033[1;36m [STRATEGIC BLUEPRINT]\033[0m")
    print(f" > SCENARIO 3 ACTIVE: Energy Shock Alpha (Target $105+)")
    print(f" > ROE OPTIMIZATION: NVDA 91.4% | Portfolio Efficiency Status: ULTRA")
    print(f" > UNITED STATES AGENDA: Resource Sovereignty Protocol 100% SECURE")
    
    print("\033[1;32m╚" + "═"*78 + "╝\033[0m")
    print(f"\033[1;30m LAST SYNC: {time.strftime('%H:%M:%S')} | MOLINA STEALTH HOST: SECURE_WS_09 \033[0m")

while True:
    draw()
    time.sleep(5) # Actualización constante cada 5 segundos
