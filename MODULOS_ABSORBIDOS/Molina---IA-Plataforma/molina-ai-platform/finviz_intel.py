import requests, re
print("\n--- MOLINA HOLDINGS: FINVIZ QUANT AUDIT ---")
tickers = ['XOM', 'NVDA', 'CVX']
headers = {'User-Agent': 'Mozilla/5.0'}
for t in tickers:
    try:
        r = requests.get(f"https://finviz.com/quote.ashx?t={t}", headers=headers, timeout=10).text
        cap = re.findall(r'Market Cap</td><td.*?>(.*?)</td>', r)
        pe = re.findall(r'P/E</td><td.*?>(.*?)</td>', r)
        print(f"{t:5} | Cap: {cap[0] if cap else 'N/A':10} | P/E: {pe[0] if pe else 'N/A'}")
    except:
        print(f"{t:5} | Error de Conexión")
print("-" * 43)
