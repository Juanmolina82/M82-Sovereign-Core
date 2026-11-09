#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TG_TOKEN = "8600412468:AAHLLRdPus6OVIhSgDkbmGCS2dWKDUfP3Y"
CHAT_ID = "-1004335849125"
NTFY_URL = "https://ntfy.sh/M82-Molina-Alerts-v3"

def push_event(source, headline, alpha_score, tag_trigger):
    if not os.path.exists(DB_PATH):
        return
    
    # 1. Inserción con 'INSERT OR IGNORE' para evadir restricciones de unicidad
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=60000;")
        cur = conn.cursor()
        
        # Sello temporal dinámico para unicidad en caso de requerir nuevos eventos
        timestamp_str = datetime.datetime.now().strftime("%H:%M:%S ET")
        full_headline = f"[{timestamp_str}] {headline}"

        cur.execute("""
            INSERT OR IGNORE INTO m82_multi_stream 
            (daemon_source, headline, status, alpha_score, asset_impact, event_trigger)
            VALUES (?, ?, 'LIVE', ?, 'TRUMP_RUBIO_MCM_REBUILD', ?)
        """, (source, full_headline, alpha_score, tag_trigger))
        
        inserted = cur.rowcount > 0
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[!] DB Error: {e}")
        return

    # 2. Despachar a Telegram / ntfy solo si el evento fue NUEVO
    if inserted:
        caption_html = (
            f"<b>⚡ #M82 DANEKA AUTO-PUSH :: TRUMP / RUBIO TRACKER</b>\n"
            f"───────────────────────────\n"
            f"🏛 <b>SOURCE:</b> {source}\n"
            f"📰 <b>HEADLINE:</b> {full_headline}\n"
            f"📊 <b>ALPHA SCORE:</b> {alpha_score} | <b>TRIGGER:</b> {tag_trigger}\n"
            f"🛡 <b>GOVERNANCE:</b> MCM 2026 | WACC 7.5% Target\n\n"
            f"<i>SOVEREIGN EXECUTION CORE — CARACAS LIBRE — MEIB Nashville ⊗ JMM Caracas</i>"
        )

        try:
            url_tg = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
            requests.post(url_tg, data={
                'chat_id': CHAT_ID,
                'text': caption_html,
                'parse_mode': 'HTML'
            }, timeout=8)
        except Exception as e:
            print(f"[!] Telegram Dispatch Warning: {e}")

        try:
            ntfy_payload = f"DANEKA PUSH [{source}]: {headline}"
            requests.post(NTFY_URL, data=ntfy_payload.encode('utf-8'), timeout=5)
        except Exception as e:
            print(f"[!] ntfy Warning: {e}")

        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ DANEKA PUSH NEW: {source} -> {tag_trigger}")

def main_loop():
    print("🚀 [DANEKA TRACKER] Motor Continuo Anticolisión Iniciado...")
    while True:
        try:
            brent_mock = 115.85
            if brent_mock >= 115.0:
                push_event(
                    "REFINITIV_OIL_DESK",
                    f"Brent ${brent_mock} 5M High — Off-Hormuz Hedge Active — Merey 16 Parity $93.92 ITM",
                    0.95,
                    "BRENT_HORMUZ_THRESHOLD_BREACH"
                )

            push_event(
                "TRUMP_RUBIO_DESK",
                "[TRACKING] Trump Gold Deal $150M Minerven/Trafigura — Rubio eval Qatar bridge $2BN — Iran threat active",
                0.99,
                "TRUMP_RUBIO_STEP"
            )

        except Exception as err:
            print(f"[!] Loop Exception: {err}")
            
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
