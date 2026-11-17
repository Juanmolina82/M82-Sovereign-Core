#!/usr/bin/env python3
import os
import time
import sqlite3
import requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
HUB_URL = "http://127.0.0.1:8286/api/workspace/ingest"

RULES = [
    ("TOP_NEWS", "INDICES_VOL", [
        "SPX", "SPY", "NDX", "QQQ", "DJI", "RUT", "IWM", "VIX", "MOVE",
        "0DTE", "GAMMA", "CREDIT CRUNCH", "CRITICAL", "ALERT", "BUNKER", "DOSSIER", "LOCKOUT"
    ]),
    ("COMPANIES", "EQUITIES_GICS", [
        "NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "AMD", "ASML",
        "JPM", "GS", "MS", "BAC", "WFC", "BLK", "BRK", "XOM", "CVX", "SLB",
        "RTX", "LMT", "BA", "CAT", "GE", "UNH", "LLY", "JNJ",
        "NKE", "ONON", "LULU", "ADS", "DECK", "UAA", "SKX", "CROX", "VFC", "PVH", "RL", "TPR", "DKS", "FL", "ASO", "JD", "BABA", "PDD", "AMZN", "WMT", "COST", "TGT", "HD", "LOW", "MCD", "SBUX", "CMG", "APPAREL", "SPORTSWEAR", "RETAIL", "WHOLESALE", "WMT", "COST", "HD",
        "RIO", "BHP", "FCX", "COIN", "EARNINGS", "GUIDANCE", "INVESTOR DAY", "M&A", "IPO"
    ]),
    ("TRENDING_TOPICS", "RATES_MACRO_FX", [
        "FED", "FOMC", "POWELL", "WARSH", "CPI", "PCE", "NFP", "GDP",
        "TREASURY", "US10Y", "US2Y", "US30Y", "YIELD", "SPREAD", "SOFR", "REPO",
        "ECB", "BOJ", "PBOC", "DXY", "EURUSD", "USDJPY", "USDCNY",
        "OPEC", "HORMUZ", "CENTCOM", "OFAC", "SANCTIONS", "TARIFF", "AI", "SEMICONDUCTOR"
    ]),
    ("LATEST_NEWS", "COMMODITIES_CRYPTO", [
        "WTI", "BRENT", "MEREY", "NYMEX", "ICE", "NATGAS", "HENRY HUB", "TTF", "CRACK",
        "GOLD", "XAU", "SILVER", "XAG", "COPPER", "PLATINUM", "PALLADIUM",
        "URANIUM", "LITHIUM", "RARE EARTH", "WHEAT", "CORN", "SOYBEAN",
        "BTC", "BITCOIN", "ETH", "ETHEREUM", "SOL", "CRYPTO", "ETF"
    ]),
    ("MOST_READ", "INSTITUTIONAL_ALPHA", [
        "MOST READ", "13F", "BUYBACK", "UPGRADE", "DOWNGRADE", "CONSENSUS", "ALPHA"
    ])
]

def classify_wallstreet(src, hdl):
    text = f" {src} {hdl} ".upper()
    for tab, asset_class, keywords in RULES:
        if any(kw in text for kw in keywords):
            return tab, asset_class
    return "LATEST_NEWS", "MULTI_ASSET"

def sync_cycle():
    last_id = 0
    while True:
        try:
            conn = sqlite3.connect(DB_PATH, timeout=60.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=60000;")
            cur = conn.cursor()
            rows = cur.execute(
                "SELECT id, daemon_source, headline FROM m82_multi_stream WHERE id > ? ORDER BY id ASC LIMIT 30",
                (last_id,)
            ).fetchall()
            conn.close()

            for rid, src, hdl in rows:
                last_id = max(last_id, rid)
                tab, asset_class = classify_wallstreet(src or "", hdl or "")
                requests.post(
                    HUB_URL,
                    json={
                        "tab": tab,
                        "headline": hdl,
                        "sector": f"{asset_class} // {src or 'LSEG'}",
                        "alpha_score": 0.92
                    },
                    timeout=5
                )
        except Exception as e:
            print(f"[!] WallStreet Sync Error: {e}", flush=True)
        time.sleep(15)

if __name__ == "__main__":
    print("🏛️ M82 WALL STREET MULTI-ASSET CLASSIFIER (:8286) ACTIVE", flush=True)
    sync_cycle()
