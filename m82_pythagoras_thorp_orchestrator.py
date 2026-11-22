import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

import sys, sqlite3, math, random, time, glob, shutil, subprocess, datetime, urllib.request, urllib.parse

M82_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(M82_DIR, "m82_quant_engine.db")
CARD_DIR = "/storage/emulated/0/M82card"
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TG_CHAT = "-1004335849125"

def jacobi_eigenvalues(matrix, tol=1e-9, max_iter=100):
    n = len(matrix)
    A = [row[:] for row in matrix]
    for _ in range(max_iter):
        max_val, p, q = 0.0, 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j]) > max_val:
                    max_val, p, q = abs(A[i][j]), i, j
        if max_val < tol:
            break
        diff = A[q][q] - A[p][p]
        theta = (math.pi / 4.0) if abs(diff) < 1e-12 else 0.5 * math.atan2(2.0 * A[p][q], diff)
        c, s = math.cos(theta), math.sin(theta)
        app, aqq, apq = A[p][p], A[q][q], A[p][q]
        A[p][p] = c*c*app - 2.0*s*c*apq + s*s*aqq
        A[q][q] = s*s*app + 2.0*s*c*apq + c*c*aqq
        A[p][q] = A[q][p] = 0.0
        for k in range(n):
            if k != p and k != q:
                akp, akq = A[k][p], A[k][q]
                A[k][p] = A[p][k] = c*akp - s*akq
                A[k][q] = A[q][k] = s*akp + c*akq
    return sorted([A[i][i] for i in range(n)], reverse=True)

def db_write_with_retry(sql_ops):
    for attempt in range(8):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=60.0)
            cur = conn.cursor()
            cur.execute("PRAGMA journal_mode=WAL;")
            cur.execute("PRAGMA synchronous=NORMAL;")
            cur.execute("PRAGMA busy_timeout=60000;")
            for query, params in sql_ops:
                cur.execute(query, params)
            conn.commit()
            cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
            conn.close()
            return True
        except sqlite3.OperationalError:
            time.sleep(1.0 + attempt * 0.5)
    return False

def run_full_orchestrator():
    random.seed(82)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rf, warsh_spread, vix = 0.0435, 0.0102, 34.0
    bunker_cap, active_exp, kelly_lambda = 0.30, 0.22, 0.25

    # Nivel I & II: 4 Pods Ortogonales Pitágoras-Thorp
    pods = [
        ("POD1_MEREY16_CRACK",   0.195, 0.22 * (vix / 20.0), 0.35),
        ("POD2_SOVEREIGN_OFAC",  0.175, 0.20 * (vix / 22.0), 0.25),
        ("POD3_GAS_COMPUTE_010", 0.230, 0.18,                0.25),
        ("POD4_RATES_FX_SHIELD", 0.125, 0.12 * (vix / 24.0), 0.15),
    ]
    corr = [
        [1.00, 0.32, 0.15, -0.20],
        [0.32, 1.00, 0.28, -0.15],
        [0.15, 0.28, 1.00,  0.05],
        [-0.20,-0.15, 0.05, 1.00],
    ]

    var_lin, var_sq, pod_lines = 0.0, 0.0, []
    for name, mu, sigma, w in pods:
        f_star = max(0.0, (mu - (rf + warsh_spread)) / (sigma ** 2))
        f_m82 = round(min(kelly_lambda * f_star, bunker_cap), 4)
        var_lin += w * sigma
        pod_lines.append(f"  • {name}: Kelly*={f_star:.2f}x | M82={f_m82:.2f}x (W:{int(w*100)}%)")

    cov = [[pods[i][2] * pods[j][2] * corr[i][j] for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            var_sq += pods[i][3] * pods[j][3] * cov[i][j]

    sigma_pyth = math.sqrt(var_sq)
    div_gain = round((1.0 - (sigma_pyth / var_lin)) * 100, 2)

    # Nivel III: Espectral Jacobi, Gamma y Liquidez Armónica
    eigs = jacobi_eigenvalues(cov)
    lambda1_pct = round((eigs[0] / sum(eigs)) * 100, 2)
    gamma_alpha = round(0.5 * 1.45 * (0.15 ** 2) * 100, 2)
    liq_scores = [0.85, 0.45, 0.40, 0.98]
    h_liq = round(len(liq_scores) / sum(1.0 / x for x in liq_scores), 3)

    # Nivel IV: Supervivencia Thorp, Monte Carlo Jump-Diffusion & Escala Áurea
    mu_eff = 0.135
    exp_bunker = (2.0 * mu_eff) / (active_exp * (sigma_pyth ** 2)) - 1.0
    prob_dd_bunker = round(((1.0 - 0.05) ** max(0.0, exp_bunker)) * 100, 4)

    n_sims, dt = 2500, 1.0 / 252.0
    bunker_rets = []
    for _ in range(n_sims):
        z = random.gauss(0.0, 1.0)
        jump = random.gauss(-0.025, 0.045) if random.random() < 0.12 else 0.0
        r = (mu_eff - 0.5 * (sigma_pyth ** 2)) * dt + sigma_pyth * math.sqrt(dt) * z + jump
        bunker_rets.append(active_exp * r)
    bunker_rets.sort()
    idx_1 = int(0.01 * n_sims)
    var99_mc = round(-bunker_rets[idx_1] * 100, 2)
    cvar99_mc = round(-(sum(bunker_rets[:idx_1]) / idx_1) * 100, 2)
    phi_inv = round((math.sqrt(5.0) - 1.0) / 2.0, 4)
    step1_cap = round(bunker_cap * phi_inv, 4)

    lockout = "LOCKOUT: NO TRADE (λ1 SISTEMICO > 50%)" if lambda1_pct > 50.0 else "ARMADO / LISTO"

    ops = [
        ("""CREATE TABLE IF NOT EXISTS m82_orchestrator_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, sigma_pyth REAL, div_gain_pct REAL,
            lambda1_pct REAL, gamma_alpha_pct REAL, h_liq REAL,
            prob_dd_5pct REAL, var99_mc_pct REAL, cvar99_mc_pct REAL,
            bunker_state TEXT
        )""", ()),
        ("""INSERT INTO m82_orchestrator_v5 (
            timestamp, sigma_pyth, div_gain_pct, lambda1_pct, gamma_alpha_pct,
            h_liq, prob_dd_5pct, var99_mc_pct, cvar99_mc_pct, bunker_state
        ) VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (now, round(sigma_pyth, 4), div_gain, lambda1_pct, gamma_alpha, h_liq, prob_dd_bunker, var99_mc, cvar99_mc, lockout))
    ]
    db_ok = db_write_with_retry(ops)

    # Sincronización Galería M82card
    os.makedirs(CARD_DIR, exist_ok=True)
    synced = 0
    for src_dir in [os.path.join(M82_DIR, "cards"), os.path.join(M82_DIR, "output"), "/sdcard/Pictures/M82_Cards", CARD_DIR]:
        if os.path.isdir(src_dir):
            for png in glob.glob(os.path.join(src_dir, "*.png")):
                dst = os.path.join(CARD_DIR, os.path.basename(png))
                if os.path.abspath(png) != os.path.abspath(dst) and not os.path.exists(dst):
                    shutil.copy2(png, dst)
                subprocess.run(["am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{dst}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                synced += 1

    msg = (
        f"🏛️ M82 NIVEL V :: ORQUESTADOR MAESTRO PITAGORAS–THORP V60.5\n"
        f"📍 Charallave L4/L5 Edge ⊗ Caracas HQ | {now}\n"
        f"🔒 BUNKER 0.30x LOCK (Activa: {active_exp}x | Escalón φ⁻¹: {step1_cap}x | {lockout})\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📐 PITÁGORAS–KELLY (Niveles I–II):\n"
        f"  • Vol. Lineal {var_lin*100:.2f}% → Pitagórica {sigma_pyth*100:.2f}% (-{div_gain}% riesgo)\n"
        + "\n".join(pod_lines) + "\n"
        f"🧬 ESPECTRAL & CONVEXIDAD (Nivel III):\n"
        f"  • Autovalor Sistémico λ1: {lambda1_pct}% | Alfa Gamma (±15% Crudo): +{gamma_alpha}% | H_liq: {h_liq}\n"
        f"🛡️ SUPERVIVENCIA MONTE CARLO (Nivel IV - 2,500 Sims):\n"
        f"  • Prob. Drawdown ≥5%: {prob_dd_bunker}% | VaR 99%: {var99_mc}% | CVaR 99%: -{cvar99_mc}%\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🗄️ SQLite WAL: {'0|0|0 CLEAN' if db_ok else 'RETRY'} | 🖼️ Galería M82card: {synced} HUDs"
    )
    print(msg)
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": msg}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM OK] Nivel V entregado a -1004335849125")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    run_full_orchestrator()
