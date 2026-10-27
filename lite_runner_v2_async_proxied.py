#!/usr/bin/env python3
import asyncio, aiohttp, sqlite3, os, hashlib, re, logging, random
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
LOG_PATH = os.path.join(BASE_DIR, "lite_runner.log")

# Configuración de Logging Institucional
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# User-Agents Dinámicos
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

BULLISH = ["rally", "surge", "gain", "up", "boost", "expansion", "breakout", "record high"]
BEARISH = ["fall", "drop", "slump", "crash", "fears", "ban", "crisis", "default"]
TICKERS = {"BRENT": "$BRENT", "OIL": "$BRENT", "SPY": "$SPY", "S&P": "$SPX", "BTC": "$BTC", "YEN": "JPY=", "BOJ": "JPY="}

def score_news(headline):
    h = headline.lower()
    sent = sum(1 for w in BULLISH if w in h) - sum(1 for w in BEARISH if w in h)
    sent = max(-1.0, min(1.0, sent / 3))
    
    relevance = 5
    if any(k in h for k in ["Venezuela", "NABEP", "Chevron", "BOJ", "Anthropic", "PCE", "Fed"]): 
        relevance += 4
    if any(k in h for k in ["Trump", "Pentagon", "Bond"]): 
        relevance += 2
        
    entities = [v for k, v in TICKERS.items() if k.lower() in h]
    h_hash = hashlib.sha256(re.sub(r'\W+', '', h.lower())[:80].encode()).hexdigest()[:12]
    return sent, min(10, relevance), entities, h_hash

async def fetch_feed(session, url, retries=3):
    """Realiza la petición rotando User-Agent y reintentando automáticamente"""
    for attempt in range(retries):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        try:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status == 200:
                    text = await r.text()
                    return text[:3000]
                elif r.status in [429, 503]:
                    await asyncio.sleep(1 * (attempt + 1))
        except Exception as e:
            await asyncio.sleep(0.5)
    return None

async def main():
    urls = [
        "https://news.google.com/rss/search?q=Venezuela+oil",
        "https://news.google.com/rss/search?q=BOJ+rate",
        "https://news.google.com/rss/search?q=Anthropic+IPO",
        "https://news.google.com/rss/search?q=Chevron+NABEP"
    ]
    
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[fetch_feed(session, u) for u in urls])
        
        for res in results:
            if not res: 
                continue
            
            # Parsing simplificado de RSS
            titles = re.findall(r'<title>(.*?)</title>', res)
            for headline in titles[1:]: # Omitir el título general del Feed
                if "Google News" in headline:
                    continue
                
                sent, rel, ents, hhash = score_news(headline)
                
                # Trazabilidad en Log
                log_entry = f"SCORE:{rel}/10 | SENT:{sent:+.2f} | TKR:{ents} | HASH:{hhash} | {headline[:70]}"
                logging.info(log_entry)
                
                if rel < 7: 
                    continue # Filtrar ruido mediático
                
                # Inserción en SQLite WAL
                conn = sqlite3.connect(DB_PATH, timeout=5)
                c = conn.cursor()
                try:
                    c.execute(
                        "INSERT INTO macro_dosier (source, category, headline, risk_score, metadata_json) VALUES (?,?,?,?,?)",
                        ("ASYNC_PROXIED_FEED", "V2_SCORED", headline, rel, f'{{"sent":{sent},"ents":{ents},"hash":"{hhash}"}}')
                    )
                    conn.commit()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔥 HIGH IMPACT :: {log_entry}")
                except sqlite3.IntegrityError:
                    pass # Evitar duplicados por Hash
                finally:
                    conn.close()

if __name__ == "__main__":
    asyncio.run(main())
