import time, os, yfinance as yf, requests, random, math
from datetime import datetime

G, W, R, GR, C, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[0m'

def draw_header():
    os.system('clear')
    print(f"{G}█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█{RS}")
    print(f"{G}█{RS} {W}MOLINA HOLDINGS LLC | STRATEGIC PACE v14.3 | {datetime.now().strftime('%H:%M:%S')}{RS}    {G}█{RS}")
    print(f"{G}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{RS}")

def get_market_data():
    assets = {"^IXIC": "NASDAQ", "BTC-USD": "BTC", "DX-Y.NYB": "DXY", "CL=F": "CRUDE", "^VIX": "FEAR_IX", "GLD": "GOLD", "XLK": "TECH", "XLE": "ENERGY"}
    try:
        data = yf.download(list(assets.keys()), period="1d", interval="1m", progress=False, threads=True)['Close']
        rows = []
        tickers = list(assets.keys())
        n_pct = ((data["^IXIC"].iloc[-1] - data["^IXIC"].iloc[0]) / data["^IXIC"].iloc[0]) * 100
        b_pct = ((data["BTC-USD"].iloc[-1] - data["BTC-USD"].iloc[0]) / data["BTC-USD"].iloc[0]) * 100
        v_inv = math.sqrt(n_pct**2 + b_pct**2)
        for i in range(0, len(tickers), 2):
            line = ""
            for j in range(2):
                if i + j < len(tickers):
                    t = tickers[i+j]; curr = data[t].dropna().iloc[-1]
                    prev = data[t].dropna().iloc[0]; pct = ((curr - prev) / prev) * 100
                    color = GR if pct >= 0 else R; sym = "▲" if pct >= 0 else "▼"
                    line += f"{C}{assets[t].ljust(8)}{W}{curr:>9.2f} {color}{sym}{pct:>5.2f}%{RS} │ "
            rows.append(f"  █ {line}")
        return rows, v_inv
    except: return [f"{R}  [!] RE-ESTABLECIENDO CONEXIÓN...{RS}"], 0

def main():
    start_ts = time.time()
    while True:
        draw_header()
        rows, v_inv = get_market_data()
        print(f"\n{G}  [ MONITOR DE ACTIVOS - MODO ESTRATÉGICO ]{RS}")
        for row in rows: print(row)
        print(f"\n{C}  [ MAGNITUD DE INVERSIÓN (V_inv) ]{RS}\n  {W}FORMULA: sqrt(x² + y²)  =>  MAGNITUD: {v_inv:.4f}{RS}")
        print(f"\n{G}█{' BÚNKER ACTIVO - VELOCIDAD MODERADA ':▀^61}█{RS}")
        print(f"\n{W}  [ SISTEMA ] {G}REFRESH:{RS} 10.0s  {G}STATUS:{RS} OPTIMAL")
        time.sleep(10.0)

if __name__ == '__main__':
    main()
