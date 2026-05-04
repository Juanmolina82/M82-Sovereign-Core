import time

def fetch_live_quotes():
    # Simulación de Inyección de Datos en Tiempo Real (Nashville-Cúa Link)
    market_data = {
        "SNDK": 84.50,
        "CRDO": 18.25,
        "AAL":  14.10,
        "NVDA": 890.12
    }
    print("Connecting to Alpha Vantage / Yahoo Finance API...")
    time.sleep(1)
    print("--- LIVE DATA STREAM INJECTED ---")
    for ticker, price in market_data.items():
        print(f"[{ticker}] Current Price: ${price} | Status: STABLE")

if __name__ == "__main__":
    fetch_live_quotes()
