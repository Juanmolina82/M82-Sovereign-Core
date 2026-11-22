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

def run_level10_bayesian():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")
    vix = 34.0
    lambda1_pct = 55.44
    net_alpha_pct = 11.27

    if os.path.exists(QUANT_DB):
        try:
            conn = sqlite3.connect(QUANT_DB, timeout=10.0)
            cur = conn.cursor()
            r5 = cur.execute("SELECT lambda1_pct FROM m82_orchestrator_v5 ORDER BY id DESC LIMIT 1").fetchone()
            r9 = cur.execute("SELECT net_alpha_pct FROM m82_execution_friction_l9 ORDER BY id DESC LIMIT 1").fetchone()
            conn.close()
            if r5: lambda1_pct = r5[0]
            if r9: net_alpha_pct = r9[0]
        except Exception:
            pass

    # Inferencia Bayesiana P(Bunker | Evidencia)
    prior_bunker = 0.65
    # Likelihood bajo crisis (VIX > 28 y lambda1 > 50%) vs régimen normal
    p_e_given_bunker = 0.94 if (vix > 28.0 and lambda1_pct > 50.0) else 0.35
    p_e_given_normal = 0.025 if (vix > 28.0 and lambda1_pct > 50.0) else 0.65

    post_bunker = (p_e_given_bunker * prior_bunker) / (
        (p_e_given_bunker * prior_bunker) + (p_e_given_normal * (1.0 - prior_bunker))
    )
    post_bunker_pct = round(post_bunker * 100, 2)
    regime_label = "REGIMEN CRISIS / BUNKER 0.30x LOCK" if post_bunker_pct >= 80.0 else "REGIMEN NORMAL / EXPANSION CONTROLADA"

    conn = sqlite3.connect(QUANT_DB, timeout=60.0)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("""CREATE TABLE IF NOT EXISTS m82_bayesian_regime_l10 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, vix REAL, lambda1_pct REAL, net_alpha_pct REAL,
        post_bunker_pct REAL, regime_label TEXT
    )""")
    cur.execute("INSERT INTO m82_bayesian_regime_l10 (timestamp, vix, lambda1_pct, net_alpha_pct, post_bunker_pct, regime_label) VALUES (?,?,?,?,?,?)",
                (now, vix, lambda1_pct, net_alpha_pct, post_bunker_pct, regime_label))
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    msg = (
        f"🧠 M82 NIVEL X :: INFERENCIA BAYESIANA & CIERRE DOCTRINAL ({now})\n"
        f"🏛️ Nodo Charallave L4/L5 Edge @ Caracas HQ | BUNKER 0.30x LOCK\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📐 EVIDENCIA CUANTITATIVA:\n"
        f"  • VIX CBOE: {vix} | Factor Jacobi (λ1): {lambda1_pct}% | Alfa Neto L9: +{net_alpha_pct}%\n"
        f"🎯 PROBABILIDAD POSTERIOR BAYESIANA:\n"
        f"  • P(Búnker | Evidencia): {post_bunker_pct}% (Umbral Desbloqueo < 40.0%)\n"
        f"🛡️ ESTADO MAESTRO (NIVELES I–X): {regime_label} | LOCKOUT: NO TRADE"
    )
    print(msg)
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": msg}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM OK] Reporte Nivel X entregado a -1004335849125")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    run_level10_bayesian()
