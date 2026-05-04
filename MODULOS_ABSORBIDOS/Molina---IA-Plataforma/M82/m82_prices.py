import yfinance as yf
import time, os, datetime
G, W, R, GR, C, B, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[0m'
def main():
    assets = {"^IXIC":"NASDAQ","SPY":"S&P500","DX-Y.NYB":"DXY","CL=F":"OIL","BTC-USD":"BTC"}
    while True:
        os.system('clear')
        print(f"{G}█ M82 PRICES | {datetime.datetime.now().strftime('%H:%M:%S')} █{RS}\n")
        try:
            data = yf.download(list(assets.keys()), period="1d", interval="1m", progress=False)['Close']
            for t, n in assets.items():
                curr = data[t].dropna().iloc[-1]
                prev = data[t].dropna().iloc[-2]
                color = GR if curr > prev else R
                print(f" {C}{n.ljust(10)}{W}{curr:>10.2f} {color}{'▲' if curr>prev else '▼'}{RS}")
        except: print(f"{R} Reintentando enlace...{RS}")
        time.sleep(1)
if __name__ == "__main__": main()
