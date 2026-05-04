import yfinance as yf
import os

def check_ormuz():
    # Tickers clave: Brent y tu dato de NVDA
    tickers = {"BRENT": "BZ=F", "NVIDIA": "NVDA"}
    os.system('clear')
    print("--- ALERTA GEOPOLÍTICA M82: ESTRECHO DE ORMUZ ---")
    for name, ticker in tickers.items():
        data = yf.Ticker(ticker).fast_info
        price = data['last_price']
        print(f"{name:10}: ${price:>8.2f} | STATUS: LIVE")
    print("-" * 45)
    print("Molina Holdings: Inteligencia de Campo Nashville")

if __name__ == "__main__":
    check_ormuz()
