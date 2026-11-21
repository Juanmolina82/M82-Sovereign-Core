#!/usr/bin/env python3
"""
================================================================================
 M82 CHARALLAVE L4/L5 EDGE // LSEG WORKSPACE NEWSMON RDP CONNECTOR
================================================================================
 Query: l:en AND (Source:DJN OR Source:MKTW OR Source:PENS OR Source:WSJ
        OR Source:IBD OR Source:BRN OR Source:FNL OR Source:WSJP)
 Mode:  HeadlineOnly=True | Repositories: NewsWire, NewsRoom, WebNews
================================================================================
"""
import datetime
import json
import os
import sys
import time
import requests

BASE_DIR = os.path.expanduser("~/M82")
CFG_PATH = os.path.join(BASE_DIR, "refinitiv-data.config.json")
sys.path.insert(0, BASE_DIR)

try:
    from core_ingestor import ingest_event
except ImportError:
    ingest_event = None

LSEG_QUERY = (
    "l:en AND ( Source:DJN OR Source:MKTW OR Source:PENS OR Source:WSJ "
    "OR Source:IBD OR Source:BRN OR Source:FNL OR Source:WSJP )"
)

HIGH_RISK_KEYWORDS = {
    "VIX": 1.6, "FED": 1.5, "COOK": 1.4, "RATE HIKE": 1.8, "WARSH": 1.5,
    "SOX": 1.4, "SEMICONDUCTOR": 1.3, "CITGO": 1.8, "PDVSA": 1.7,
    "VENEZUELA": 1.6, "OFAC": 1.7, "SANCTIONS": 1.5, "IRAN": 1.6,
    "OIL": 1.3, "CRUDE": 1.3, "IMF": 1.4, "DEBT": 1.3, "CRASH": 2.0,
    "DEFAULT": 2.0, "TARIFF": 1.4, "RECESSION": 1.6,
}

def load_lseg_creds():
    if not os.path.exists(CFG_PATH):
        return None
    with open(CFG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    sessions = data.get("sessions", {}).get("platform", {})
    rdp = sessions.get("news", sessions.get("rdp", {}))
    return {
        "username": rdp.get("username", "jmmp@molina82.com"),
        "password": rdp.get("password", ""),
        "app_key": rdp.get("app-key", rdp.get("app_key", "")),
    }

def get_rdp_access_token(creds: dict) -> str:
    url = "https://api.refinitiv.com/auth/oauth2/v1/token"
    payload = {
        "username": creds["username"],
        "password": creds["password"],
        "grant_type": "password",
        "scope": "trapi",
        "takeExclusiveSignOnControl": "true",
        "client_id": creds["app_key"],
    }
    res = requests.post(url, data=payload, timeout=15)
    res.raise_for_status()
    return res.json()["access_token"]

def score_headline(headline: str):
    up = headline.upper()
    score = 5.5
    matched = []
    for kw, weight in HIGH_RISK_KEYWORDS.items():
        if kw in up:
            score += weight
            matched.append(kw)
    score = min(round(score, 2), 9.9)
    cat = "GEOPOLITICS_ENERGY" if any(k in matched for k in ["CITGO", "PDVSA", "VENEZUELA", "OFAC", "IRAN", "OIL", "CRUDE"]) else "MACRO_MARKETS_WIRE"
    tag = "BUNKER_030X_CRITICAL" if score >= 8.0 else "LSEG_WIRE_WATCH"
    return score, cat, tag, ",".join(matched[:6]) or "DJN_WSJ_WIRE"

def fetch_lseg_newsmon(limit: int = 15):
    creds = load_lseg_creds()
    if not creds or not creds.get("password") or not creds.get("app_key"):
        print("⚠️ Credenciales RDP incompletas en ~/M82/refinitiv-data.config.json.")
        return 0

    token = get_rdp_access_token(creds)
    url = "https://api.refinitiv.com/data/news/v1/headlines"
    params = {
        "query": LSEG_QUERY,
        "limit": limit,
    }
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, params=params, headers=headers, timeout=15)
    res.raise_for_status()
    items = res.json().get("data", [])

    inserted = 0
    for item in items:
        nv = item.get("newsItem", {}).get("itemMeta", {})
        content_meta = item.get("newsItem", {}).get("contentMeta", {})
        headline = (
            item.get("headline")
            or content_meta.get("headline", [{}])[0].get("$", "")
            or ""
        ).strip()
        if not headline:
            continue

        risk_score, category, m82_tag, entities = score_headline(headline)
        if ingest_event:
            ok = ingest_event(
                source="LSEG_NEWSMON_RDP",
                category=category,
                headline=headline,
                risk_score=risk_score,
                sentiment=-0.35 if risk_score >= 8.0 else 0.0,
                entities=entities,
                m82_tag=m82_tag,
                desk="CHARALLAVE_L4_L5_EDGE",
            )
            if ok:
                inserted += 1
        else:
            print(f"[DRY-RUN Risk={risk_score}] {headline}")

    print(f"📡 [LSEG NEWSMON] Barrido completado ({datetime.now(datetime.timezone.utc).strftime('%H:%M:%S UTC')}) | Nuevos titulares: {inserted}/{len(items)}")
    return inserted

if __name__ == "__main__":
    try:
        fetch_lseg_newsmon(limit=15)
    except Exception as e:
        print(f"⚠️ [LSEG NEWSMON] Error de conexión RDP: {e}")

    if "--daemon" in sys.argv:
        while True:
            time.sleep(180)
            try:
                fetch_lseg_newsmon(limit=15)
            except Exception as e:
                print(f"⚠️ [LSEG NEWSMON LOOP] {e}")
