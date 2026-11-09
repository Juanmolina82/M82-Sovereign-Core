#!/usr/bin/env python3
import sqlite3, os, json, urllib.request, urllib.parse, requests

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
CARD_PATH = os.path.join(BASE_DIR, "card_output.png")

TELEGRAM_TOKEN = os.getenv("M82_TELEGRAM_TOKEN", "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y")
TELEGRAM_CHAT_ID = os.getenv("M82_CHAT_ID", "-1004335849125")
NYFT_ENDPOINT = os.getenv("NYFT_ENDPOINT", os.getenv("NFIT_ENDPOINT", "http://127.0.0.1:8080/api/alerts"))

def execute_dispatch():
    if not os.path.exists(DB_PATH):
        print("❌ Base de datos m82_database.db no encontrada.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT headline, source, category, risk_score, m82_tag, metadata_json, sentiment, entities 
        FROM macro_dosier 
        ORDER BY id DESC LIMIT 1;
    """)
    row = c.fetchone()
    conn.close()

    if not row:
        print("⚠️ No hay registros en macro_dosier.")
        return

    headline, source, category, risk, tag, meta_json, sentiment, entities = row

    # --- 1. FORMATO DE TEXTO ---
    caption_text = (
        f"🚨 *#M82 BREAKING [{tag}]*\n\n"
        f"📌 *Titular:* {headline}\n"
        f"📊 *Risk Score:* {risk}/10.0 | *Fuente:* {source}\n"
        f"🏷️ *Categoría:* {category}\n"
        f"🎯 *Entidades:* {entities}\n\n"
        f"🛡️ _AGI Quantum Verified // @MolinaHoldings LLC_"
    )

    print("--------------------------------------------------")
    print("📝 TEXTO DE LA ALERTA PREPARADO:")
    print(caption_text)
    print("--------------------------------------------------\n")

    # --- 2. ENVÍO A TELEGRAM (IMAGEN + CAPTION TEXT) ---
    url_tg = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    headers_tg = {"Content-Type": f"multipart/form-data; boundary={boundary}"}

    if os.path.exists(CARD_PATH):
        with open(CARD_PATH, 'rb') as f:
            img_bytes = f.read()

        body = []
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{TELEGRAM_CHAT_ID}\r\n".encode())
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption_text}\r\n".encode())
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"parse_mode\"\r\n\r\nMarkdown\r\n".encode())
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"card.png\"\r\nContent-Type: image/png\r\n\r\n".encode())
        body.append(img_bytes)
        body.append(f"\r\n--{boundary}--\r\n".encode())

        req = urllib.request.Request(url_tg, data=b"".join(body), headers=headers_tg)
        try:
            urllib.request.urlopen(req, timeout=12)
            print("✅ [TELEGRAM] Alerta e imagen con texto transmitidas exitosamente al canal.")
        except Exception as e:
            print(f"❌ [TELEGRAM] Error de envío a Telegram: {e}")
    else:
        print("❌ [TELEGRAM] No se encontró card_output.png")

    # --- 3. ENVÍO A NYFT / NFIT (JSON PAYLOAD) ---
    nyft_payload = {
        "event_id": tag,
        "source": source,
        "category": category,
        "risk_score": risk,
        "headline": headline,
        "sentiment": sentiment,
        "entities": entities,
        "metadata": json.loads(meta_json) if meta_json else {},
        "status": "VERIFIED_HIGH_RISK",
        "node": "CHARALLAVE_EDGE_M82"
    }

    try:
        r = requests.post(NYFT_ENDPOINT, json=nyft_payload, headers={'Content-Type': 'application/json'}, timeout=5)
        print(f"✅ [NYFT] Alerta transmitida exitosamente a NYFT (Status: {r.status_code}).")
    except Exception as e:
        print(f"⚠️ [NYFT] No se pudo conectar con el endpoint NYFT ({NYFT_ENDPOINT}): {e}")
        print("ℹ️ Asigna la variable NYFT_ENDPOINT con la URL/IP exacta de tu API de NYFT.")

if __name__ == "__main__":
    execute_dispatch()
