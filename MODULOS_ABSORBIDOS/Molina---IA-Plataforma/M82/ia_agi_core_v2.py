import time, os, yfinance as yf, threading, random
from datetime import datetime

# Paleta M82: Contraste Militar
G, W, R, GR, C, B, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[0m'

class GlobalCommand:
    def __init__(self):
        # Sectores Complementarios (No repetidos del monitor 1)
        self.sectors = {
            "GLOBAL INDICES ": {"^GDAXI":"DAX_40", "^FTSE":"FTSE_100", "^N225":"NIKKEI_225", "^HSI":"HANG_SENG", "^FCHI":"CAC_40"},
            "INDUSTRIAL METALS": {"HG=F":"COPPER", "PL=F":"PLATINUM", "PA=F":"PALLADIUM", "ALI=F":"ALUMINUM", "LIT":"LITHIUM_ETF"},
            "FIXED INCOME/YLD": {"^TNX":"US_10Y_BOND", "^TYX":"US_30Y_BOND", "^FVX":"US_5Y_BOND", "TIP":"INFL_PROT", "AGG":"AGGR_BOND"},
            "GROWTH LEADERS ": {"LLY":"ELI_LILLY", "AVGO":"BROADCOM", "ASML":"ASML_HLD", "TMO":"THERMO_FISH", "NVO":"NOVO_NORD"},
            "RETAIL & CONS  ": {"WMT":"WALMART", "COST":"COSTCO", "HD":"HOME_DEPOT", "PG":"P&G_CORP", "KO":"COCA_COLA"},
            "DEFENSE & AERO ": {"LMT":"LOCKHEED", "RTX":"RAYTHEON", "BA":"BOEING", "NOC":"NORTHROP", "GD":"GEN_DYNAM"}
        }
        self.data = {n: {"v": 0.0, "p": 0.0} for s in self.sectors.values() for n in s.values()}
        self.news_stream = [
            "ALERTA: Irán declara el Estrecho de Hormuz 'Abierto' temporalmente hasta el 22 de abril.",
            "MARKET: Bitcoin salta a 8,000 tras señales de alivio geopolítico en Medio Oriente.",
            "ELI LILLY: Capitalización récord; el sector Biotech se posiciona como el hedge del 2026.",
            "FIXED INCOME: Los rendimientos del Tesoro reaccionan al discurso de Trump en Islamabad.",
            "ASML: Suministro de máquinas High-NA EUV se normaliza; impulso para TSMC y Intel."
        ]
        self.is_running = True

    def engine(self):
        all_tickers = [t for s in self.sectors.values() for t in s.keys()]
        while self.is_running:
            try:
                raw = yf.download(all_tickers, period="1d", interval="1m", progress=False)['Close']
                for sect, assets in self.sectors.items():
                    for t, n in assets.items():
                        series = raw[t].dropna()
                        if not series.empty:
                            curr, prev = series.iloc[-1], series.iloc[0]
                            self.data[n] = {"v": curr, "p": ((curr-prev)/prev)*100}
                if random.random() > 0.8:
                    self.news_stream.append(self.news_stream.pop(0))
            except: pass
            time.sleep(12)

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{G}█{' MOLINA HOLDINGS | GLOBAL COMMAND CONSOLE v130.0 ':▀^60}█{RS}")
            for sect_name, assets in self.sectors.items():
                print(f"\n{C}▼ {sect_name}{RS}")
                print(f"{W}────────────────────────────────────────────────────────────{RS}")
                assets_list = list(assets.values())
                for i in range(0, len(assets_list), 2):
                    line = ""
                    for j in range(2):
                        if i + j < len(assets_list):
                            n = assets_list[i+j]
                            d = self.data[n]
                            color = GR if d['p'] >= 0 else R
                            val = f"{d['v']:>9.2f}" if d['v'] < 1000 else f"{d['v']:>9.1f}"
                            line += f"{W}{n[:10].ljust(10)}{RS} {B}{val}{RS} {color}{d['p']:>+6.2f}%{RS} | "
                    print(f" {line}")

            print(f"\n{G}── [ DOSSIER COMPLEMENTARIO M82 ] ──────────────────────────{RS}")
            print(f" {W}MONITOR:{RS} {B}02-SECUNDARIO{RS} | {W}PRIO:{RS} {GR}ESTRATÉGICA{RS} | {W}HORMUZ:{RS} {GR}OPEN_TEMP{RS}")
            
            print(f"\n{R}⚡ GLOBAL NEWS & MACRO PULSE (2026):{RS}")
            for i, msg in enumerate(self.news_stream[:3]):
                print(f" {W}{i+1}. {msg}{RS}")
            
            print(f"\n{G}█{' ESTATUS: VIGILANCIA GLOBAL ACTIVA ':▀^60}█{RS}")
            time.sleep(10)

if __name__ == "__main__":
    t = GlobalCommand()
    threading.Thread(target=t.engine, daemon=True).start()
    t.display()
