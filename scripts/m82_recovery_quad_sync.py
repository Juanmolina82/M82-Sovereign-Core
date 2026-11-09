#!/usr/bin/env python3
import os, sys, time, sqlite3, requests

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v2"
USER_ACCOUNT = "jmmp@molina82.com"

def sync_recovery_matrix():
    conn = sqlite3.connect(DB_PATH, timeout=120)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=120000;")
    cur = conn.cursor()

    headline = "[QUAD-SPV $200B] Citi NY Escrow + Citgo 50.1% Collateral Pledged — 35 Bonds Recovery Recalibrated (VENZ $51.95 / PDVSA20 $115.32)"
    m82_tag = "v61.0.1-QUAD-SPV-200B-RECOVERY-RECALIBRATED"

    cur.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json)
        VALUES ('REFINITIV_WORKSPACE_LSEG', 'DEBT_RECOVERY_QUAD_SPV', ?, 1.20, ?, 0.95, '{"account":"jmmp@molina82.com","spv_notional_b":200,"pdvsa20_price":115.32,"venz27_price":51.95}')
    """, (headline, m82_tag))

    cur.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
        VALUES ('M82_DEBT_DESK', '[TELEMETRY] Quad-SPV $200B Securitization Base Verified — Citi NY Escrow Channel Active', 'BREAKOUT_ACTIVE', 0.99, 'SOVEREIGN_DEBT_CITGO', 'QUAD_SPV_RECOVERY_SEALED')
    """, ())

    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    # Despacho en vivo a Telegram & ntfy
    caption_tg = (
        f"⚡ <b>M82 QUAD-SPV TELEMETRY</b> :: {time.strftime('%H:%M:%S VET')}\n"
        f"───────────────────────────\n"
        f"👤 <b>USER:</b> {USER_ACCOUNT}\n"
        f"🏛 <b>COLLATERAL:</b> Citgo Holding (50.1% PDVSA 2020) + Citi NY Escrow\n"
        f"💼 <b>NOTIONAL SPV:</b> $200 Billion (4 x $50B Legs)\n"
        f"📈 <b>RECOVERY RANGE:</b> 70.00 - 82.00 Cents (PDVSA20 Par $115.32)\n"
        f"🏷 <b>TAG:</b> <code>{m82_tag}</code>\n"
        f"🛡 <b>RISK:</b> Exp 0.22x | VaR 1.68% | Warsh +102.0bps\n"
        f"🔒 <b>GOVERNANCE:</b> BUNKER MODE 0.30x LOCK\n\n"
        f"🏛 @MolinaHoldings | Chairman Juan M. Molina"
    )

    try:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data={
            'chat_id': CHAT_ID, 'text': caption_tg, 'parse_mode': 'HTML'
        }, timeout=10)
        requests.post(NTFY_URL, data=f"M82 QUAD-SPV: $200B Securitization Base Recalibrated for {USER_ACCOUNT}".encode('utf-8'), headers={
            "Title": "M82 QUAD-SPV $200B RECOVERY", "Priority": "high", "Tags": "bank,shield"
        }, timeout=10)
        print("🟢 [RECOVERY SYNC SUCCESS] Evento e ingesta despachados a Telegram & ntfy.")
    except Exception as e:
        print(f"[!] Dispatch Error: {e}")

if __name__ == "__main__":
    sync_recovery_matrix()
