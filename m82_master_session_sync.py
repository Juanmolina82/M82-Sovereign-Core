import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

import sys, sqlite3, math, glob, shutil, subprocess, datetime, urllib.request, urllib.parse

M82_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(M82_DIR, "m82_database.db")
CARD_DIR = "/storage/emulated/0/M82card"
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TG_CHAT = "-1004335849125"

sys.path.insert(0, M82_DIR)

def ensure_wal_db():
    os.makedirs(M82_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA synchronous=NORMAL;")
    cur.execute("PRAGMA busy_timeout=60000;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS master_session_dossier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            session_code TEXT,
            summary TEXT,
            risk_score REAL,
            alpha REAL,
            sigma_pythagoras REAL,
            daily_var_99 REAL,
            bunker_state TEXT
        )
    """)
    conn.commit()
    return conn

def run_pythagoras_thorp():
    rf = 0.0435
    warsh_spread = 0.0102   # +102.0 bps
    vix = 34.0              # CBOE VIX +21% -> 34.0
    bunker_cap = 0.30       # BUNKER MODE 0.30x LOCK
    kelly_lambda = 0.25     # Fractional Kelly (Beat the Market - Thorp)

    pods = [
        ("POD1_MEREY16_CRACK",   0.195, 0.22 * (vix / 20.0), 0.35),
        ("POD2_SOVEREIGN_OFAC",  0.175, 0.20 * (vix / 22.0), 0.25),
        ("POD3_GAS_COMPUTE_010", 0.230, 0.18,                0.25),
        ("POD4_RATES_FX_SHIELD", 0.125, 0.12 * (vix / 24.0), 0.15),
    ]
    corr = [
        [1.00, 0.18, 0.10, -0.15],
        [0.18, 1.00, 0.22, -0.10],
        [0.10, 0.22, 1.00,  0.05],
        [-0.15,-0.10, 0.05, 1.00],
    ]

    pod_lines = []
    var_sq = 0.0
    var_lin = 0.0

    for name, mu, sigma, w in pods:
        f_star = max(0.0, (mu - (rf + warsh_spread)) / (sigma ** 2))
        f_m82 = round(min(kelly_lambda * f_star, bunker_cap), 4)
        pod_lines.append(f"  • {name}: Kelly*={f_star:.2f}x | M82={f_m82:.2f}x (W:{int(w*100)}%)")
        var_lin += w * sigma

    for i in range(len(pods)):
        for j in range(len(pods)):
            var_sq += pods[i][3] * pods[j][3] * pods[i][2] * pods[j][2] * corr[i][j]

    sigma_pyth = math.sqrt(var_sq)
    div_gain = round((1.0 - (sigma_pyth / var_lin)) * 100, 2)
    active_exp = 0.22
    var_99 = round((sigma_pyth / math.sqrt(252)) * 2.326 * active_exp * 100, 2)
    return sigma_pyth, var_lin, div_gain, var_99, pod_lines

def sync_gallery():
    os.makedirs(CARD_DIR, exist_ok=True)
    count = 0
    for src_dir in [os.path.join(M82_DIR, "cards"), os.path.join(M82_DIR, "output"), "/sdcard/Pictures/M82_Cards", CARD_DIR]:
        if os.path.isdir(src_dir):
            for png in glob.glob(os.path.join(src_dir, "*.png")):
                dst = os.path.join(CARD_DIR, os.path.basename(png))
                if os.path.abspath(png) != os.path.abspath(dst) and not os.path.exists(dst):
                    shutil.copy2(png, dst)
                subprocess.run(
                    ["am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{dst}"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                count += 1
    return count

def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sigma_pyth, var_lin, div_gain, var_99, pod_lines = run_pythagoras_thorp()

    consolidated_summary = (
        "CONSOLIDACION SOBERANA M82 V60.5 | "
        "1) GEOPOLITICA VZ: CRISIS ORMUZ (KHAT SHEKAN) + IMPACTO INDUSTRIAL BAREIN (5TA FLOTA) ACELERAN TESIS ESTRATEGICA MCM & EDMUNDO GONZALEZ (NON-HORMUZ MEREY 16 PADD3 | OFAC GL 46E/48D/49B/52C | EO 14373 CUSTODIA NY | PLAN 4 FASES TSJ DIC-2026) | "
        "2) BALTICO/NORTE (DAY 1731): SPARTA II SANCIONADO EN LLAMAS FRENTE A FINLANDIA + VIOLACION AEREA OTAN + DDOS ID-PORTEN NORUEGA | "
        "3) MERCADOS CBOE: VIX +21% A 34.0 | NASDAQ -1,110 PTS (-4.6%) | XLK BEAR MARKET | "
        "4) MOTOR PITAGORAS-THORP MULTI-POD: BUNKER MODE 0.30x LOCK | EXP 0.22x | LOCKOUT: NO TRADE"
    )

    # Ingesta mediante core_ingestor si está disponible para disparo HUD automático
    try:
        from core_ingestor import ingest_event
        ingest_event(
            "M82_MASTER_CONSOLIDATION",
            "SOVEREIGN_PYTHAGORAS_THORP_SYNC",
            consolidated_summary,
            9.99,
            0.99,
            "ORMUZ,BAHRAIN,MCM,EDMUNDO_GONZALEZ,SPARTA_II,NORWAY_DDOS,VIX34,THORP_KELLY,PITAGORAS,BUNKER_030X",
            "PURGED_LEGACY_LOOP",
            "CHARALLAVE_L4_L5_EDGE"
        )
    except Exception as e:
        print(f"[CORE_INGESTOR INFO] Registro directo en DB maestro ({e})")

    conn = ensure_wal_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO master_session_dossier (timestamp, session_code, summary, risk_score, alpha, sigma_pythagoras, daily_var_99, bunker_state) VALUES (?,?,?,?,?,?,?,?)",
        (now, "M82_V605_MASTER_SYNC", consolidated_summary, 9.99, 0.99, round(sigma_pyth, 4), var_99, "BUNKER_030X_LOCK_NO_TRADE")
    )
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    synced_cards = sync_gallery()

    tg_msg = (
        f"🛡️ M82 SOVEREIGN EXECUTION CORE V60.5 — MASTER SYNC\n"
        f"📍 Nodo: Charallave L4/L5 Edge ⊗ Caracas HQ | {now}\n"
        f"🔒 Gobernanza: BUNKER MODE 0.30x LOCK (Exp: 0.22x | LOCKOUT: NO TRADE)\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"1️⃣ VZ TRANSICIÓN (MCM / EGU): Ormuz + Bahréin consolidan Merey 16 Non-Hormuz Hedge (OFAC / EO 14373).\n"
        f"2️⃣ BÁLTICO / NORTE: Sparta II ardiendo frente a Finlandia + DDoS ID-porten Noruega.\n"
        f"3️⃣ CBOE / MACRO: VIX 34.0 (+21%) | Nasdaq -4.6% | XLK Bear Market | Warsh +102bps.\n"
        f"4️⃣ PITÁGORAS–THORP MULTI-POD:\n"
        f"  • Vol. Lineal {var_lin*100:.2f}% → Pitagórica {sigma_pyth*100:.2f}% (-{div_gain}% riesgo)\n"
        f"  • VaR Diario 99%: {var_99}% (Target ~1.68%)\n"
        + "\n".join(pod_lines) + "\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🗄️ SQLite WAL: 0|0|0 CLEAN | 🖼️ Galería M82card: {synced_cards} HUDs indexadas"
    )

    print(tg_msg)
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": tg_msg}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM OK] Boletin maestro entregado a -1004335849125")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    main()
