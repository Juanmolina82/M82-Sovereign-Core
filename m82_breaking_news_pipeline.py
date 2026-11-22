import os, sys, sqlite3, datetime, urllib.request, urllib.parse

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

M82_DIR = os.path.expanduser("~/M82")
QUANT_DB = os.path.join(M82_DIR, "m82_quant_engine.db")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TG_CHAT = "-1004335849125"

def ingest_cable(theater: str, headline: str, impact: str, x_post: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")
    conn = sqlite3.connect(QUANT_DB, timeout=60.0)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("""CREATE TABLE IF NOT EXISTS m82_geopolitical_intel_stream (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, theater TEXT, headline TEXT, mesa_impact TEXT
    )""")
    cur.execute("INSERT INTO m82_geopolitical_intel_stream (timestamp, theater, headline, mesa_impact) VALUES (?,?,?,?)",
                (now, theater, headline, impact))
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    x_clean = x_post[:240]
    with open(os.path.join(M82_DIR, "logs", "x_post_latest.txt"), "w", encoding="utf-8") as f:
        f.write(x_clean + "\n")

    msg = (
        f"📡 M82 CABLE / BREAKING INTEL ({now})\n"
        f"🏛️ Teatro: {theater} | BUNKER 0.30x LOCK\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📰 CABLE: {headline}\n"
        f"🛡️ IMPACTO MESA: {impact}\n"
        f"🐦 X POST ({len(x_clean)}/240 chars): {x_clean}"
    )
    print(msg)
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": msg}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM OK] Cable auditado y despachado.")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
        post = f"Alerta macro en desarrollo: {raw[:155]}. M82 mantiene gobernanza BUNKER 0.30x LOCK y Dry Powder blindado ante volatilidad sistémica. #Macro #M82"
        ingest_cable("CUSTOM_WIRE", raw, "EVALUACIÓN NIVELES VIII-X ACTIVA", post)
