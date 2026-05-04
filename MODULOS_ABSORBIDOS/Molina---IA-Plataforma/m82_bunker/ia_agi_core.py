import time, os, yfinance as yf, threading
from datetime import datetime

# Estética Molina Holdings - High Performance
G, W, R, GR, C, B, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[0m'

class IntelligenceOverlordV260:
    def __init__(self):
        self.sectors = {
            "1": {"NAME": "GLOBAL INDICES", "TICKERS": {"^DJI":"DOW_JONES", "^IXIC":"NASDAQ", "^GSPC":"S&P_500", "^N225":"NIKKEI_225", "^VIX":"FEAR_INDEX"}, "KEY": "ECONOMY"},
            "2": {"NAME": "TECH LEADERS", "TICKERS": {"AAPL":"APPLE", "MSFT":"MICROSOFT", "NVDA":"NVIDIA", "TSM":"TSMC", "AVGO":"BROADCOM"}, "KEY": "AI"},
            "3": {"NAME": "ENERGY & BANK", "TICKERS": {"XOM":"EXXON_MOB", "SHEL":"SHELL_PLC", "JPM":"JP_MORGAN", "GS":"GOLD_SACHS", "CVX":"CHEVRON"}, "KEY": "FED"},
            "4": {"NAME": "DEFENSE CORP", "TICKERS": {"LMT":"LOCKHEED", "RTX":"RAYTHEON", "NOC":"NORTHROP", "GD":"GEN_DYNA", "BA":"BOEING"}, "KEY": "WAR"},
            "5": {"NAME": "SUPPLY CHAIN", "TICKERS": {"MAERSK-B.CO":"MAERSK", "ZIM":"ZIM_INT", "UPS":"UPS_LOG", "HLAG.DE":"HAPAG-L", "BDRY":"BALTIC_DRY"}, "KEY": "SHIPPING"},
            "6": {"NAME": "CYBER DEFENSE", "TICKERS": {"CRWD":"CROWDSTK", "PANW":"PALO_ALTO", "FTNT":"FORTINET", "ZS":"ZSCALER", "OKTA":"OKTA_INC"}, "KEY": "CYBERSECURITY"},
            "7": {"NAME": "NUCLEAR/URANIUM", "TICKERS": {"CCJ":"CAMECO", "UUUU":"ENERGY_FU", "URNM":"URAN_ETF", "SMR":"NU_SCALE", "BWXT":"BWX_TECH"}, "KEY": "URANIUM"},
            "8": {"NAME": "LUXURY & ALPHA", "TICKERS": {"MC.PA":"LVMH", "RMS.PA":"HERMES", "RACE":"FERRARI", "KER.PA":"KERING", "LRLCF":"RALPH_LAU"}, "KEY": "LUXURY"},
            "9": {"NAME": "HEALTH GLOBAL", "TICKERS": {"LLY":"ELI_LILLY", "NVO":"NOVO_NORD", "UNH":"UNITED_H", "JNJ":"J&J_CORP", "ABBV":"ABBVIE"}, "KEY": "BIOTECH"}
        }
        self.data = {}
        self.news = []
        self.selected = "1"
        self.is_running = True
        self._init_data()

    def _init_data(self):
        for s in self.sectors.values():
            for n in s['TICKERS'].values():
                self.data[n] = {"v": 0.0, "p": 0.0, "vol": 0}

    def sync_data(self):
        all_t = [t for s in self.sectors.values() for t in s['TICKERS'].keys()]
        while self.is_running:
            try:
                raw = yf.download(all_t, period="1d", interval="1m", progress=False, group_by='ticker', threads=True)
                for s in self.sectors.values():
                    for t, n in s['TICKERS'].items():
                        try:
                            df = raw[t].dropna()
                            if not df.empty:
                                val, prev = df['Close'].iloc[-1], df['Close'].iloc[0]
                                self.data[n] = {"v": val, "p": ((val-prev)/prev)*100, "vol": int(df['Volume'].iloc[-1])}
                        except: continue
            except: pass
            time.sleep(12)

    def sync_news(self):
        while self.is_running:
            try:
                # El motor de noticias ahora busca el Ticker líder del sector seleccionado
                target_t = list(self.sectors[self.selected]['TICKERS'].keys())[0]
                n_raw = yf.Ticker(target_t).news
                temp_news = []
                for item in n_raw[:5]:
                    ts = datetime.fromtimestamp(item['providerPublishTime']).strftime('%H:%M') if 'providerPublishTime' in item else datetime.now().strftime('%H:%M')
                    temp_news.append(f"[{ts}] {item['publisher'].upper()}: {item['title']}")
                self.news = temp_news
            except: pass
            time.sleep(30)

    def run(self):
        while self.is_running:
            os.system('clear')
            print(f"{G}█{' MOLINA HOLDINGS | INTELLIGENCE OVERLORD v260 ':▀^65}█{RS}")
            
            # Selector de Sectores
            for k, v in self.sectors.items():
                marker = f"{G}▶{RS}" if self.selected == k else " "
                perf = sum([self.data[n]['p'] for n in v['TICKERS'].values()]) / 5
                print(f" {marker} {W}[{k}]{RS} {B}{v['NAME']:<18}{RS} | {GR if perf >= 0 else R}{perf:>+6.2f}%{RS}")

            # Desglose de Equities ORDENADO POR VOLUMEN
            s = self.sectors[self.selected]
            print(f"\n{C}▼ SECTOR: {s['NAME']} (Sorted by High-Volume/Capital){RS}")
            print(f"{W}{'EQUITY':<12} | {'PRICE':<10} | {'VAR%':<8} | {'VOLUME (INSTIT)'}{RS}")
            print(f"{W}─────────────────────────────────────────────────────────────────{RS}")
            
            # Algoritmo de ordenamiento
            sorted_items = sorted(s['TICKERS'].items(), key=lambda x: self.data[x[1]]['vol'], reverse=True)
            
            for t, n in sorted_items:
                d = self.data[n]
                print(f"{B}{n[:12]:<12}{RS} | {W}{d['v']:>10.2f}{RS} | {GR if d['p'] >= 0 else R}{d['p']:>+7.2f}%{RS} | {G}{d['vol']:>15,}{RS}")

            # Bloque de Noticias Dinámico
            print(f"\n{R}⚡ BREAKING NEWS: {s['NAME']}{RS}")
            print(f"{W}─────────────────────────────────────────────────────────────────{RS}")
            for m in self.news:
                print(f" {W}• {m[:75]}...{RS}")

            print(f"\n{G}Toca (1-9) para cambiar | '0' para reset/salir{RS}")
            cmd = input(f"{C}M82_TOUCH > {RS}").strip()
            if cmd == '0': self.is_running = False
            elif cmd in self.sectors:
                self.selected = cmd
                self.news = ["SINCRONIZANDO FEED SECTORIAL..."]

if __name__ == "__main__":
    ui = IntelligenceOverlordV260()
    threading.Thread(target=ui.sync_data, daemon=True).start()
    threading.Thread(target=ui.sync_news, daemon=True).start()
    ui.run()
