import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

import sqlite3, datetime, urllib.request, urllib.parse

M82_DIR = os.path.expanduser("~/M82")
QUANT_DB = os.path.join(M82_DIR, "m82_quant_engine.db")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TG_CHAT = "-1004335849125"

def run_sunday_sentinel():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")
    vix = 34.0
    warsh_bps = 102.0
    active_exp = 0.22
    bunker_cap = 0.30

    # Leer última métrica espectral (Nivel V) y frontera óptima (Nivel VII)
    lambda1_pct, sharpe_opt, var99_opt = 51.84, 1.10, 0.41
    if os.path.exists(QUANT_DB):
        try:
            conn = sqlite3.connect(QUANT_DB, timeout=30.0)
            r5 = conn.execute("SELECT lambda1_pct FROM m82_orchestrator_v5 ORDER BY id DESC LIMIT 1").fetchone()
            r7 = conn.execute("SELECT sharpe_opt, var99_opt_pct FROM m82_dynamic_frontier_l7 ORDER BY id DESC LIMIT 1").fetchone()
            conn.close()
            if r5:
                lambda1_pct = r5[0]
            if r7:
                sharpe_opt, var99_opt = r7[0], r7[1]
        except Exception:
            pass

    # Regla determinista de desbloqueo de apertura dominical (18:00 VET)
    unlock_ready = (vix < 28.0) and (lambda1_pct < 50.0)
    regime_state = "ARMADO / LISTO PARA EJECUCION" if unlock_ready else "LOCKOUT: NO TRADE (BLINDAJE ACTIVO)"

    conn = sqlite3.connect(QUANT_DB, timeout=60.0)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("""CREATE TABLE IF NOT EXISTS m82_sunday_sentinel_l8 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, vix REAL, lambda1_pct REAL,
        sharpe_opt REAL, var99_opt_pct REAL, regime_state TEXT
    )""")
    cur.execute("INSERT INTO m82_sunday_sentinel_l8 (timestamp, vix, lambda1_pct, sharpe_opt, var99_opt_pct, regime_state) VALUES (?,?,?,?,?,?)",
                (now, vix, lambda1_pct, sharpe_opt, var99_opt, regime_state))
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    msg = (
        f"🛡️ M82 NIVEL VIII :: SENTINEL DE APERTURA DOMINICAL ({now})\n"
        f"📍 Nodo Charallave L4/L5 Edge ⊗ Caracas HQ | BUNKER {bunker_cap}x LOCK\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• Régimen CBOE: VIX {vix} | Warsh Spread: +{warsh_bps} bps | Exp. Activa: {active_exp}x\n"
        f"• Factor Sistémico Jacobi (λ1): {lambda1_pct}% (Umbral Desbloqueo: < 50.0%)\n"
        f"• Frontera Óptima Nivel VII: Sharpe {sharpe_opt} | VaR 99% Diario: {var99_opt}%\n"
        f"• Vectores Vigilados: Ormuz/Bahréin (Merey 16 PADD 3) | Báltico Sparta II / DDoS Noruega\n"
        f"🚦 DECISIÓN DE MESA: {regime_state}"
    )
    print(msg)
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": msg}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM OK] Sentinel Nivel VIII entregado a -1004335849125")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    run_sunday_sentinel()
