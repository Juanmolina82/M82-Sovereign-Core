import time, os, yfinance as yf, threading
from datetime import datetime

G, W, R, GR, C, B, Y, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[93m', '\033[0m'

class M82FuturesTerminal:
    def __init__(self):
        self.is_running = True
        self.report_path = os.path.expanduser("~/M82/archive/daily_report.txt")
        # FUTUROS CONTINUOS (Activos 23/5 durante el After-Hours)
        self.tickers = {
            "ES=F": "S&P_500_FUTURES",
            "NQ=F": "NASDAQ_100_FUT",
            "BZ=F": "BRENT_CRUDE_FUT",
            "CL=F": "WTI_CRUDE_FUT",
            "GC=F": "GOLD_FUTURES"
        }
        self.data = {n: {"v": 0.0, "p": 0.0, "t": ""} for n in self.tickers.values()}

    def sync_futures(self):
        """Captura de alta frecuencia para Futuros"""
        while self.is_running:
            for t_id, n in self.tickers.items():
                try:
                    # Usamos period 1d e interval 1m para forzar el último tick del after-hours
                    t = yf.Ticker(t_id)
                    hist = t.history(period="1d", interval="1m")
                    if not hist.empty:
                        last_price = float(hist['Close'].iloc[-1])
                        prev_close = float(t.fast_info.previous_close)
                        change = ((last_price - prev_close) / prev_close) * 100
                        self.data[n] = {
                            "v": last_price, 
                            "p": change, 
                            "t": datetime.now().strftime("%H:%M:%S")
                        }
                except:
                    continue
            time.sleep(5) # Refresco de seguridad para evitar baneo de IP

    def display(self):
        while self.is_running:
            os.system('clear')
            print(f"{C}█{' M82 REAL-TIME FUTURES | AFTER-HOURS SESSION ':▀^65}█{RS}")
            print(f" {W}CHAIRMAN:{RS} {B}JUANMOLINA82{RS} | {G}STATUS: TRADING RESUMED{RS}")
            print(f" {Y}STRATEGY:{RS} {W}MONITORING TRUMP CEASEFIRE IMPACT{RS}")
            
            print(f"\n{W}{'FUTUROS (LIVE)':<20} | {'PRECIO':>12} | {'VAR %'}{RS}")
            print(f" {W}{'-'*55}{RS}")
            
            for n, d in self.data.items():
                color = GR if d['p'] >= 0 else R
                print(f" {W}• {n:<18} | {B}{d['v']:>12.2f}{RS} | {color}{d['p']:>+8.2f}%{RS}")

            print(f"\n{B}▼ INTELIGENCIA DE MERCADO:{RS}")
            if self.data['S&P_500_FUTURES']['p'] > 0.3:
                print(f" {GR}[UP] Los futuros confirman rally de alivio tras extensión de tregua.{RS}")
            if self.data['BRENT_CRUDE_FUT']['v'] > 97:
                print(f" {R}[WARN] El crudo no baja de 97. La amenaza de Irán sigue pesando.{RS}")

            print(f"\n{G}0 EXIT | Nashville-Valencia Secured | {self.data['S&P_500_FUTURES']['t']}{RS}")
            cmd = input(f"{C}M82_COMMAND > {RS}").strip()
            if cmd == '0': self.is_running = False

if __name__ == "__main__":
    terminal = M82FuturesTerminal()
    threading.Thread(target=terminal.sync_futures, daemon=True).start()
    terminal.display()
