#!/usr/bin/env python3
import os, sys, time, sqlite3, requests
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
USER_ACCOUNT = "jmmp@molina82.com"

def ingest_and_dispatch():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    headline = "[BLOOMBERG / LSEG] GE Vernova Awaits Upfront Payment Before Starting Venezuela Power Grid Repairs — CEO Scott Strazik (SEN Rebuild Est. $25B)"
    m82_tag = "v61.0.1-GE-VERNOVA-GEV-POWER-GRID-PAYMENT-LOCK"

    cur.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json)
        VALUES ('REFINITIV_WORKSPACE_LSEG', 'INFRASTRUCTURE_POWER_GRID', ?, 1.75, ?, 0.88, '{"account":"jmmp@molina82.com","ticker":"GEV.N","ceo":"Scott Strazik","capex_est_b":25.0}')
    """, (headline, m82_tag))

    cur.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
        VALUES ('M82_INFRA_DESK', '[TELEMETRY] GE Vernova Upfront Payment Lock Validates Citi Escrow $200B Capital Ingestion Requirement', 'BREAKOUT_ACTIVE', 0.97, 'POWER_GRID_INFRASTRUCTURE', 'GE_VERNOVA_PAYMENT_WAIT')
    """, ())

    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    # Formato de Despacho Móvil
    caption_tg = (
        f"⚡ <b>M82 LSEG WIRE TELEMETRY</b> :: {time.strftime('%H:%M:%S VET')}\n"
        f"───────────────────────────\n"
        f"👤 <b>USER:</b> {USER_ACCOUNT}\n"
        f"🏛 <b>SOURCE:</b> Bloomberg / Refinitiv Workspace (GEV.N)\n"
        f"📂 <b>CATEGORY:</b> INFRASTRUCTURE_POWER_GRID\n"
        f"📰 <b>HEADLINE:</b> GE Vernova (CEO Scott Strazik) exige pago por adelantado antes de iniciar reparaciones de la red eléctrica en Venezuela ($25B SEN Rebuild).\n"
        f"🏷 <b>TAG:</b> <code>{m82_tag}</code>\n"
        f"🛡 <b>RISK:</b> Exp 0.22x | VaR 1.68% | Warsh +102.0bps\n"
        f"🔒 <b>GOVERNANCE:</b> BUNKER MODE 0.30x LOCK\n\n"
        f"🏛 @MolinaHoldings | Chairman Juan M. Molina"
    )

    try:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={
            'chat_id': CHAT_ID, 'text': caption_tg, 'parse_mode': 'HTML'
        }, timeout=10)
        requests.post(NTFY_URL, data=f"LSEG WIRE [{USER_ACCOUNT}]: GE Vernova awaits Venezuela payment for power grid repairs".encode('utf-8'), headers={
            "Title": "M82 INFRA: GE VERNOVA SEN LOCK", "Priority": "high", "Tags": "zap,shield"
        }, timeout=10)
        print("🟢 [GE VERNOVA INGEST SUCCESS] Evento registrado en BBDD local y despachado a Telegram/ntfy.")
    except Exception as e:
        print(f"[!] Dispatch Error: {e}")

if __name__ == "__main__":
    ingest_and_dispatch()
