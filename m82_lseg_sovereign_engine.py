#!/usr/bin/env python3
"""
M82 SOVEREIGN AUTONOMOUS LSEG / REFINITIV ENGINE (ZERO-GEMINI DEPENDENCY)
Conecta directo con LSEG Workspace / RDP API -> Motor Cuantico Local ->
SQLite WAL (App Android 8282) + Telegram Push
"""
import os
import re
import json
import time
import sqlite3
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path("/data/data/com.termux/files/home/M82")
DB_PATH = BASE_DIR / "m82_database.db"
ENV_FILE = BASE_DIR / ".lseg_sovereign.env"

TG_TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
TG_CHAT = "-1004335849125"

# Universo de instrumentos LSEG Workspace monitoreados autonomamente
RIC_UNIVERSE = [
    ".SPX", ".IXIC", ".SOX", "NVDA.O", "INTC.OQ", "TSN.N", "CNC.N",
    "LCOc1", "CLc1", "US10YT=RR", "US30YT=RR", "XAG=", "CMCU3", "BTC="
]

# Diccionario cuantitativo institucional local (sin dependencia de LLM externo)
BEARISH_WEIGHTS = {
    "fall": -0.35, "falls": -0.35, "drop": -0.35, "tumble": -0.45, "plunge": -0.50,
    "hike": -0.40, "hikes": -0.40, "hawkish": -0.40, "restrict": -0.45, "ban": -0.50,
    "block": -0.45, "war": -0.55, "attack": -0.50, "sanction": -0.45, "resign": -0.40,
    "inflation": -0.35, "selloff": -0.45, "default": -0.60, "probe": -0.35
}
BULLISH_WEIGHTS = {
    "surge": 0.40, "gain": 0.30, "rally": 0.40, "beat": 0.45, "growth": 0.30,
    "ceasefire": 0.50, "license": 0.45, "approval": 0.40, "escrow": 0.35, "record": 0.30
}
HIGH_IMPACT_ENTITIES = {
    "NVIDIA", "NVDA", "ANTHROPIC", "WARSH", "FED", "FOMC", "BRENT", "ORMUZ", "HORMUZ",
    "OFAC", "VENEZUELA", "MEREY", "CHIPS", "SEMICONDUCTOR", "SOX", "UST10Y", "TREASURY", "JPM"
}

def load_lseg_credentials():
    creds = {
        "LSEG_USERNAME": os.environ.get("LSEG_USERNAME", "jmmp@molina82.com"),
        "LSEG_PASSWORD": os.environ.get("LSEG_PASSWORD", ""),
        "LSEG_APP_KEY": os.environ.get("LSEG_APP_KEY", "")
    }
    # Intentar extraer AppKey / credenciales de scripts previos si existen
    for candidate in ("refinitiv_bridge.py", "m82_refinitiv_realtime_bridge.py", ".env", ".lseg_sovereign.env"):
        p = BASE_DIR / candidate
        if p.exists():
            txt = p.read_text(encoding="utf-8", errors="ignore")
            m_key = re.search(r'(?:APP_KEY|app_key|AppKey)["\'\s:=]+([A-Za-z0-9]{20,64})', txt)
            m_usr = re.search(r'([A-Za-z0-9._%+-]+@molina82\.com)', txt)
            m_pwd = re.search(r'(?:PASSWORD|password)["\'\s:=]+([^\s"\']+)', txt)
            if m_key and not creds["LSEG_APP_KEY"]:
                creds["LSEG_APP_KEY"] = m_key.group(1)
            if m_usr:
                creds["LSEG_USERNAME"] = m_usr.group(1)
            if m_pwd and not creds["LSEG_PASSWORD"]:
                creds["LSEG_PASSWORD"] = m_pwd.group(1)
    if not ENV_FILE.exists():
        ENV_FILE.write_text(
            f"LSEG_USERNAME={creds['LSEG_USERNAME']}\n"
            f"LSEG_PASSWORD={creds['LSEG_PASSWORD']}\n"
            f"LSEG_APP_KEY={creds['LSEG_APP_KEY']}\n",
            encoding="utf-8"
        )
        ENV_FILE.chmod(0o600)
    return creds

class LSEGDirectClient:
    def __init__(self, creds):
        self.username = creds["LSEG_USERNAME"]
        self.password = creds["LSEG_PASSWORD"]
        self.app_key = creds["LSEG_APP_KEY"]
        self.access_token = None
        self.token_expiry = 0.0

    def authenticate(self):
        if not (self.username and self.password and self.app_key):
            return False
        if self.access_token and time.time() < (self.token_expiry - 60):
            return True
        url = "https://api.refinitiv.com/auth/oauth2/v1/token"
        payload = urllib.parse.urlencode({
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
            "scope": "trapi",
            "client_id": self.app_key,
            "takeExclusiveSignOnControl": "true"
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self.access_token = data.get("access_token")
                self.token_expiry = time.time() + int(data.get("expires_in", 300))
                return bool(self.access_token)
        except Exception as e:
            print(f"[LSEG-AUTH] Aviso conexion RDP (verifique password en .lseg_sovereign.env): {e}")
            return False

    def fetch_pricing_snapshots(self, rics):
        if not self.authenticate():
            return []
        url = f"https://api.refinitiv.com/data/pricing/snapshots/v1/?universe={urllib.parse.quote(','.join(rics))}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.access_token}"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8")).get("Data", [])
        except Exception as e:
            print(f"[LSEG-PRICING] Error snapshot: {e}")
            return []

    def fetch_top_headlines(self, query="NVIDIA OR ANTHROPIC OR FED OR BRENT OR CHIPS OR WARSH", limit=8):
        if not self.authenticate():
            return []
        url = f"https://api.refinitiv.com/data/news/v1/headlines?query={urllib.parse.quote(query)}&limit={limit}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.access_token}"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8")).get("data", [])
        except Exception as e:
            print(f"[LSEG-NEWS] Error headlines: {e}")
            return []

def quant_score_headline(headline: str):
    """Motor determinista local: calcula sentiment, alpha y risk_score sin LLM externo."""
    tokens = re.findall(r"[A-Za-z0-9]+", headline.upper())
    sent = 0.0
    entity_hits = 0
    for tk in tokens:
        low = tk.lower()
        if low in BEARISH_WEIGHTS:
            sent += BEARISH_WEIGHTS[low]
        elif low in BULLISH_WEIGHTS:
            sent += BULLISH_WEIGHTS[low]
        if tk in HIGH_IMPACT_ENTITIES:
            entity_hits += 1
    sent = max(-1.0, min(1.0, round(sent, 3)))
    alpha = min(0.99, round(0.55 + (entity_hits * 0.09) + (abs(sent) * 0.25), 3))
    quant_signal = round(0.70 * alpha + 0.30 * sent, 3)
    risk_score = min(0.99, round(0.50 + (entity_hits * 0.08) + (max(0.0, -sent) * 0.35), 3))
    return sent, alpha, quant_signal, risk_score

def send_telegram_alert(msg: str):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": msg, "parse_mode": "Markdown"}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method="POST"), timeout=10) as r:
            return r.status == 200
    except Exception:
        return False

def run_cycle(client: LSEGDirectClient):
    con = sqlite3.connect(str(DB_PATH), timeout=60.0)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA busy_timeout=60000;")
    cur = con.cursor()

    # 1. Ingesta directa de precios LSEG Workspace
    snaps = client.fetch_pricing_snapshots(RIC_UNIVERSE)
    for item in snaps:
        ric = item.get("Key", {}).get("Name", "")
        fields = item.get("Fields", {})
        last_px = fields.get("TRDPRC_1") or fields.get("BID") or fields.get("PRIMACT_1")
        pct_chg = fields.get("PCTCHNG", 0.0)
        if ric and last_px is not None:
            try:
                cur.execute("""
                    INSERT OR REPLACE INTO m82_live_market_quotes (symbol, price, change_pct, source, updated_at)
                    VALUES (?, ?, ?, 'LSEG_RDP_DIRECT', datetime('now'))
                """, (ric, float(last_px), float(pct_chg or 0.0)))
            except Exception:
                pass

    # 2. Ingesta directa de titulares Reuters / LSEG + Scoring Cuantico Local
    headlines = client.fetch_top_headlines()
    for h in headlines:
        title = h.get("headline", {}).get("title", "") if isinstance(h.get("headline"), dict) else str(h.get("headline", ""))
        if not title:
            continue
        exists = cur.execute("SELECT 1 FROM macro_dossier WHERE headline LIKE ? LIMIT 1", (f"%{title[:65]}%",)).fetchone()
        if exists:
            continue
        sent, alpha, qsig, risk = quant_score_headline(title)
        cur.execute("""
            INSERT INTO macro_dossier (node_origin, governance_mode, var_daily, active_exposure, source, category, desk_cluster, headline, risk_score, m82_tag, sentiment, alpha_score, tail_risk_index)
            VALUES ('NODO_CHARALLAVE_EDGE', 'BUNKER_MODE_0.30x_LOCK', 1.68, 0.22, 'LSEG_RDP_SOVEREIGN', 'AUTONOMOUS_WIRE', 'LSEG_DIRECT_DESK', ?, ?, 'M82_SOVEREIGN_V60', ?, ?, ?)
        """, (f"[LSEG DIRECT] {title}", risk, sent, alpha, round(1.0 + risk, 2)))

        if risk >= 0.72:
            now_utc = datetime.now(timezone.utc).strftime("%H:%M UTC")
            alert = (
                f"🛰 *#M82 SOVEREIGN LSEG DIRECT* :: `{now_utc}`\n"
                f"───────────────────────────\n"
                f"📰 {title}\n"
                f"📊 *Risk:* `{risk:.2f}` | *Alpha:* `{alpha:.2f}` | *Quant:* `{qsig:+.2f}`\n"
                f"🔒 *BUNKER 0.30x LOCK* (Exp `0.22x` | VaR `1.68%`)"
            )
            send_telegram_alert(alert)

    con.commit()
    con.execute("PRAGMA wal_checkpoint(PASSIVE);")
    con.close()

if __name__ == "__main__":
    creds = load_lseg_credentials()
    print(f"=== M82 SOVEREIGN LSEG ENGINE INICIADO | User={creds['LSEG_USERNAME']} | AppKey={'OK' if creds['LSEG_APP_KEY'] else 'PENDIENTE'} ===")
    client = LSEGDirectClient(creds)
    while True:
        try:
            run_cycle(client)
        except Exception as e:
            print(f"[!] Ciclo LSEG Sovereign: {e}")
        time.sleep(60)
