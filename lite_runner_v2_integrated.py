#!/usr/bin/env python3
"""
M82 QUANTUM MACRO DOSSIER - INTEGRATED V3 FINAL
HQ: Caracas Central | NODE: Caracas HQ Node
INTEGRA: Infra Robusta V2 + Dossier V1-V15 VEN PA ACÁ PAJARITO
40 Daemons / Async / WAL / ZeroMQ / Anti-429 / M82-SCORER
"""
import asyncio, aiohttp, sqlite3, os, hashlib, re, logging, random, json
from datetime import datetime
from pathlib import Path

# ── CONFIG INSTITUCIONAL ──
BASE_DIR = Path.home() / "M82"
DB_PATH = BASE_DIR / "m82_database.db"
LOG_PATH = BASE_DIR / "lite_runner.log"

FEEDS = [
    # M82 CORE - Venezuela Oil
    "https://news.google.com/rss/search?q=Venezuela+oil+PDVSA+Chevron+NABEP+65Bn",
    "https://news.google.com/rss/search?q=PDVSA+debt+15B+Ryder+Scott+DeGolyer+reserves",
    "https://news.google.com/rss/search?q=Jose+terminal+Venezuela+bottleneck+Trinidad+Guyana+hub",
    "https://news.google.com/rss/search?q=Chevron+Petropiar+Petroboscan+Venezuela+License+41+OFAC",
    "https://news.google.com/rss/search?q=Trump+Pentagon+Venezuela+bonds+VENZ+Lazard+restructuring",
    # MACRO
    "https://news.google.com/rss/search?q=BOJ+rate+USDJPY+yen",
    "https://news.google.com/rss/search?q=Brent+crude+WTI+oil+prices",
    "https://news.google.com/rss/search?q=PCE+inflation+Fed+rates+pause",
    "https://news.google.com/rss/search?q=Anthropic+AI+IPO+shutdown+paradox"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

# ── SCORER INTEGRADO M82 ──
BULLISH = ["rally","surge","gain","up","boost","expansion","breakout","record high","rise","jump","lease","hub","investment","fresh capex"]
BEARISH = ["fall","drop","slump","crash","fears","ban","crisis","default","decline","plunge","debt","asphalt","bottleneck","no payment"]

# Diccionario M82 - Tu dossier V1-V15
M82_KEYWORDS = {
    # CRÍTICO 10/10
    "EL CARGO TE PROTEGE": 10,
    "VEN PA ACA PAJARITO": 10,
    "PDVSA DEBE 15": 10,
    "BOYACA 5/8 ASFALTO": 10,
    # ALTO 9/10
    "RYDER SCOTT": 9, "DEGOLYER": 9, "JOSE 1.8": 9, "JOSE BOTTLENECK": 9,
    "PERSONALIDAD DEL CRUDO": 9, "RECIBO PDVSA": 9, "TESORO NY": 9, "TRINIDAD HUB": 9,
    # MEDIO-ALTO 8/10
    "65BN": 8, "NABEP": 8, "PDVSA SOBRECRESIDA": 8, "BAJARLE EL COGOTE": 8,
    "MIDSTREAM": 8, "OFAC 41": 8, "MEREY": 8, "GUYANA LIVIANO": 8,
    "VALERO": 8, "MARATHON": 8, "CHEVRON LOMITO": 8
}

TICKERS = {
    "BRENT":"$BRENT","OIL":"$BRENT","SPY":"$SPY","S&P":"$SPX","BTC":"$BTC",
    "YEN":"JPY=","BOJ":"JPY=","VENZ":"VENZ","PCE":"PCE","FED":"FED",
    "PDVSA":"PDVSA","NABEP":"NABEP","CHEVRON":"CVX","MEREY":"MEREY"
}

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] HQ:Caracas NODE:Caracas | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def init_db():
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute("PRAGMA busy_timeout=5000;")
    c.execute("PRAGMA cache_size=-20000;")
    c.execute("PRAGMA synchronous=NORMAL;")
    c.execute("""
        CREATE TABLE IF NOT EXISTS macro_dosier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            source TEXT,
            category TEXT,
            headline TEXT,
            risk_score REAL,
            sentiment REAL,
            entities TEXT,
            hash TEXT UNIQUE,
            m82_tag TEXT,
            metadata_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def score_news_m82(headline: str):
    h = headline.lower()
    h_upper = headline.upper()
    sent = sum(1 for w in BULLISH if w.lower() in h) - sum(1 for w in BEARISH if w.lower() in h)
    sent = max(-1.0, min(1.0, sent / 3))

    relevance = 4
    m82_tag = "MACRO_GENERAL"
    # Check M82 keywords
    for kw, score_bonus in M82_KEYWORDS.items():
        if kw.lower() in h or kw in h_upper:
            relevance += 3
            m82_tag = kw
            if score_bonus >= 10:
                relevance = 10
                break

    if any(k.lower() in h for k in ["venezuela","nabep","chevron","boj","anthropic","pce","fed","venz","lazard","pdvsa","ryder scott"]):
        relevance += 2

    entities = [v for k,v in TICKERS.items() if k.lower() in h]
    h_hash = hashlib.sha256(re.sub(r'\W+','',h)[:80].encode()).hexdigest()[:12]
    return sent, min(10, relevance), entities, h_hash, m82_tag

async def fetch_feed(session, url, retries=3):
    for attempt in range(retries):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
            "Cache-Control": "no-cache"
        }
        try:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status == 200:
                    text = await r.text()
                    return text[:6000]
                elif r.status in [429][403][503]:
                    wait = 1.5 * (attempt+1) + random.uniform(0,1)
                    logging.warning(f"HTTP {r.status} {url} -> retry {attempt+1} in {wait:.1f}s")
                    await asyncio.sleep(wait)
                else:
                    return None
        except Exception as e:
            logging.error(f"FETCH ERR {url}: {e}")
            await asyncio.sleep(0.5 * (attempt+1))
    return None

async def process_headline(headline: str):
    if "Google News" in headline or len(headline) < 15:
        return
    sent, rel, ents, hhash, m82_tag = score_news_m82(headline)

    # Log diferenciado
    if m82_tag!= "MACRO_GENERAL":
        log_entry = f"M82_ALERT:{m82_tag} SCORE:{rel}/10 | SENT:{sent:+.2f} | TKR:{ents} | HASH:{hhash} | {headline[:90]}"
    else:
        log_entry = f"SCORE:{rel}/10 | SENT:{sent:+.2f} | TKR:{ents} | HASH:{hhash} | {headline[:90]}"
    logging.info(log_entry)

    if rel < 7:
        return

    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO macro_dosier (source, category, headline, risk_score, sentiment, entities, hash, m82_tag, metadata_json)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            "M82_INTEGRATED_V3",
            "V3_SCORED_M82" if m82_tag!= "MACRO_GENERAL" else "V3_SCORED_MACRO",
            headline,
            rel,
            sent,
            json.dumps(ents),
            hhash,
            m82_tag,
            json.dumps({"sent":sent,"ents":ents,"hash":hhash,"m82":m82_tag,"hq":"Caracas","node":"Caracas","dossier":"VEN PA ACA PAJARITO"})
        ))
        conn.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔥 {log_entry}")
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

async def main():
    init_db()
    logging.info("M82 INTEGRATED V3 START - Caracas HQ | Caracas HQ Node - M82 Dossier V1-V15 ACTIVE")

    connector = aiohttp.TCPConnector(limit=20, limit_per_host=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        results = await asyncio.gather(*[fetch_feed(session, u) for u in FEEDS])

        tasks = []
        for res in results:
            if not res:
                continue
            titles = re.findall(r'<title>(.*?)</title>', res, re.DOTALL)
            for headline in titles[1:]:
                headline = re.sub(r'<[^>]+>','',headline).strip()
                tasks.append(process_headline(headline))

        if tasks:
            await asyncio.gather(*tasks)

    print(f"✅ M82 Integrated Cycle Done - {datetime.now()} - DB: {DB_PATH}")

if __name__ == "__main__":
    asyncio.run(main())
