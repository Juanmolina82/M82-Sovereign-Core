import time, os, yfinance as yf, threading, random, subprocess
from datetime import datetime

G, W, R, GR, C, B, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[0m'

class FixedArmorSovereignty:
    def __init__(self):
        # MANTENIENDO TODOS LOS BLOQUES SOLICITADOS
        self.sectors = {
            "GLOBAL FUTURES": {"^DJI":"DOW_30", "^IXIC":"NASDAQ_100", "^SPX":"S&P_500", "^N225":"NIKKEI", "^GDAXI":"DAX_40"},
            "WAR COMMODS  ": {"CL=F":"BRENT_OIL", "GC=F":"GOLD_FUT", "SI=F":"SILVER", "HG=F":"COPPER", "NG=F":"NAT_GAS"},
            "FOREX & CRYPTO": {"DX-Y.NYB":"USD_INDEX", "EURUSD=X":"EUR_USD", "^TNX":"US_10Y_B", "BTC-USD":"BITCOIN", "ETH-USD":"ETH"},
            "AI & SEMIS   ": {"NVDA":"NVIDIA", "TSM":"TSMC", "AVGO":"BROADCOM", "ASML":"ASML_HLD", "SMCI":"SUPERMICRO"},
            "SUPPLY CHAIN ": {"MAERSK-B.CO":"MAERSK", "HLAG.DE":"HAPAG-L", "ZIM":"ZIM_INT", "BDRY":"BALTIC_DRY", "UPS":"UPS_LOG"},
            "TECH LEADERS ": {"AAPL":"APPLE", "MSFT":"MICROSOFT", "GOOGL":"ALPHABET", "AMZN":"AMAZON", "META":"META_PLAT"},
            "HEALTH GLOBAL": {"LLY":"ELI_LILLY", "NVO":"NOVO_NORD", "UNH":"UNITED_H", "JNJ":"J&J_CORP", "ABBV":"ABBVIE"},
            "ENERGY & BANK": {"XOM":"EXXON_MOB", "SHEL":"SHELL_PLC", "JPM":"JP_MORGAN", "GS":"GOLD_SACHS", "CVX":"CHEVRON"},
            "DEFENSE CORP ": {"LMT":"LOCKHEED", "RTX":"RAYTHEON", "NOC":"NORTHROP", "GD":"GEN_DYNA", "BA":"BOEING"},
            "INDUSTRIAL   ": {"TSLA":"TESLA", "BABA":"ALIBABA", "DE":"JOHN_DEERE", "CAT":"CATERPIL", "WMT":"WALMART"}
        }
        self.data = {n: {"v": 0.0, "p": 0.0} for s in self.sectors.values() for n in s.values()}
        self.news_feed = ["REPARACIÓN V152.1 COMPLETADA... ELIMINANDO ERROR 404..."]
        self.is_running = True
        self.git_backup()

    def git_backup(self):
        def _task():
            try:
                subprocess.run(["git", "add", "."], cwd=os.path.expanduser("~/M82"), capture_output=True)
                subprocess.run(["git", "commit", "-m", f"V152.1-Patch-{datetime.now().strftime('%H%M')}"], cwd=os.path.expanduser("~/M82"), capture_output=True)
                subprocess.run(["git", "push"], cwd=os.path.expanduser("~/M82"), capture_output=True)
            except: pass
        threading.Thread(target=_task, daemon=True).start()

    def fetch_live_news(self):
        watch_list = ["AAPL", "BTC-USD", "CL=F", "MAERSK-B.CO", "^IXIC"]
        while self.is_running:
            try:
                temp_news = []
                for ticker in watch_list:
                    raw_news = yf.Ticker(ticker).news
                    for n in raw_news[:2]:
                        title = n['title'].upper()
                        if any(x in title for x in ["SROUJI", "IRAN", "FED", "AI", "OIL", "ORMUZ", "BTC", "SHIPPING"]):
                            entry = f"{n['publisher']}: {n['title']}"
                            if entry not in self.news_feed: temp_news.append(entry)
                if temp_news: self.news_feed = (temp_news + self.news_feed)[:15]
            except: time.sleep(10)
            time.sleep(45)

    def engine(self):
        all_tickers = [t for s in self.sectors.values() for t in s.keys()]
        while self.is_running:
            try:
                # Descarga robusta con manejo de errores por símbolo
                raw = yf.download(all_tickers, period="1d", interval="1m", progress=False, group_by='ticker')
                for sect, assets in self.sectors.items():
                    for t, n in assets.items():
                        try:
                            series = raw[t]['Close'].dropna()
                            if not series.empty:
                                curr, prev = series.iloc[-1], series.iloc[0]
                                self.data[n] = {"v": curr, "p": ((curr-prev)/prev)*100}
                        except: continue
            except: time.sleep(5)
            time.sleep(15)

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{G}█{' MOLINA HOLDINGS | FIXED ARMOR v152.1 ':▀^65}█{RS}")
            for sect_name, assets in self.sectors.items():
                print(f"\n{C}▼ {sect_name}{RS}")
                print(f"{W}─────────────────────────────────────────────────────────────────{RS}")
                assets_list = list(assets.values())
                for i in range(0, len(assets_list), 2):
                    line = ""
                    for j in range(2):
                        if i + j < len(assets_list):
                            n = assets_list[i+j]
                            d = self.data[n]
                            color = GR if d['p'] >= 0 else R
                            val = f"{d['v']:>10.2f}" if d['v'] < 1000 else f"{d['v']:>10.1f}"
                            line += f"{W}{n[:12].ljust(12)}{RS} {B}{val}{RS} {color}{d['p']:>+6.2f}%{RS} | "
                    print(f" {line}")

            print(f"\n{G}── [ DOSSIER M82 | LOGÍSTICA & RIESGO ] ─────────────────────────{RS}")
            print(f" {W}NODE:{RS} {B}CH-01-VZLA{RS} | {W}ORMUZ:{RS} {R}CRITICAL{RS} | {W}GIT:{RS} {GR}PROTECTED{RS}")
            print(f"\n{R}⚡ LIVE BREAKING INTEL (SUPPLY CHAIN & WAR):{RS}")
            for i, msg in enumerate(self.news_feed[:4]):
                print(f" {W}{i+1}. {msg[:70]}...{RS}")
            print(f"\n{G}█{' ESTATUS: MANDO TOTAL | PROTOCOLO V152.1 ACTIVO ':▀^65}█{RS}")
            time.sleep(10)

if __name__ == "__main__":
    t = FixedArmorSovereignty()
    threading.Thread(target=t.engine, daemon=True).start()
    threading.Thread(target=t.fetch_live_news, daemon=True).start()
    t.display()
