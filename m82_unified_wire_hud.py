import os, sys, sqlite3, hashlib, datetime, urllib.request, urllib.parse

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

M82_DIR = os.path.expanduser("~/M82")
QUANT_DB = os.path.join(M82_DIR, "m82_quant_engine.db")
X_POST_OUT = os.path.join(M82_DIR, "logs", "x_post_latest.txt")

TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TG_CHAT = "-1004335849125"
NTFY_TOPIC = os.environ.get("M82_NTFY_TOPIC", "m82-sovereign-core-jmm")
REFINITIV_USER = "jmmp@molina82.com"

os.makedirs(os.path.dirname(X_POST_OUT), exist_ok=True)

def dispatch_wire(badge: str, hud_headline: str, quant_analysis: str, x_post: str, force: bool = False):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")
    wire_hash = hashlib.sha256(f"{badge}:{hud_headline}".encode("utf-8")).hexdigest()[:16]

    conn = sqlite3.connect(QUANT_DB, timeout=60.0)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA busy_timeout=60000;")
    cur.execute("""CREATE TABLE IF NOT EXISTS m82_dispatch_ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, wire_hash TEXT UNIQUE, badge TEXT,
        hud_headline TEXT, x_post TEXT
    )""")

    if not force:
        cur.execute("SELECT 1 FROM m82_dispatch_ledger WHERE wire_hash = ?", (wire_hash,))
        if cur.fetchone():
            print(f"[DEDUP OK] Cable {wire_hash} ya fue despachado.")
            conn.close()
            return

    cur.execute("INSERT OR REPLACE INTO m82_dispatch_ledger (timestamp, wire_hash, badge, hud_headline, x_post) VALUES (?,?,?,?,?)",
                (now, wire_hash, badge, hud_headline, x_post[:240]))
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    x_clean = x_post[:240]
    with open(X_POST_OUT, "w", encoding="utf-8") as f:
        f.write(x_clean + "\n")

    full_msg = (
        f"📡 M82 REFINITIV REAL-TIME WIRE [{badge}] ({now})\n"
        f"👤 Workspace: {REFINITIV_USER} | 🔒 BUNKER 0.30x LOCK\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📰 CABLE EN VIVO:\n{hud_headline}\n\n"
        f"📊 AUDITORÍA CUANTITATIVA M82 (NIVELES I–X):\n{quant_analysis}\n\n"
        f"🐦 X POST LISTO ({len(x_clean)}/240 chars):\n{x_clean}"
    )
    print(full_msg)

    # Despacho exclusivo de texto limpio a Telegram (DANEKA M82)
    try:
        url_txt = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data_txt = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": full_msg}).encode("utf-8")
        urllib.request.urlopen(url_txt, data=data_txt, timeout=10)
        print("[TELEGRAM OK] Despacho textual limpio enviado a DANEKA M82.")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

    # Despacho exclusivo de texto limpio a ntfy
    try:
        req_ntfy = urllib.request.Request(f"https://ntfy.sh/{NTFY_TOPIC}", data=full_msg.encode("utf-8"))
        req_ntfy.add_header("Title", f"M82 BREAKING [{badge}] - {REFINITIV_USER}")
        req_ntfy.add_header("Priority", "high")
        urllib.request.urlopen(req_ntfy, timeout=10)
        print(f"[NTFY OK] Push textual entregado a ntfy.sh/{NTFY_TOPIC}")
    except Exception as e:
        print(f"[NTFY WARN] {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        raw_cable = " ".join(sys.argv[1:])
        x_auto = f"BREAKING ({REFINITIV_USER}): {raw_cable[:130]}. M82 mantiene BUNKER 0.30x LOCK y Dry Powder blindado ante volatilidad. #Macro #Energy #M82"
        q_auto = "• P(Búnker|E): 99.64% | LOCKOUT: NO TRADE 18:00 VET.\n• Cobertura activa: Merey 16 Non-Hormuz + Gas-to-Compute 0.10x."
        dispatch_wire("REF_WS_LIVE", raw_cable, q_auto, x_auto, force=True)
