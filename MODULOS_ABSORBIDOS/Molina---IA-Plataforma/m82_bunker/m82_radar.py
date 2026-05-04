import requests, time, os
from bs4 import BeautifulSoup
G, W, R, GR, C, B, RS = '\033[1;93m', '\033[1;97m', '\033[1;91m', '\033[1;92m', '\033[1;96m', '\033[1m', '\033[0m'
def main():
    while True:
        os.system('clear')
        print(f"{R}█ M82 AGGRESSIVE RADAR | BREAKING NEWS █{RS}\n")
        try:
            soup = BeautifulSoup(requests.get("https://finance.yahoo.com/topic/stock-market-news/", headers={'User-Agent':'Mozilla/5.0'}).text, 'html.parser')
            news = [h.text for h in soup.find_all(['h3', 'h2']) if len(h.text) > 35][:4]
            for h in news:
                print(f" {W}📰 {h.upper()[:90]}...{RS}")
                print(f" {R if 'war' in h.lower() or 'fed' in h.lower() else C} [ANÁLISIS M82]: Verificando impacto...{RS}\n")
                time.sleep(5)
        except: time.sleep(5)
if __name__ == "__main__": main()
