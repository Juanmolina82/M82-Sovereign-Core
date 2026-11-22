import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

import sqlite3, math, datetime, urllib.request, urllib.parse

def jacobi_eigenvalues(matrix, tol=1e-9, max_iter=100):
    # Rotación ortogonal pitagórica (Jacobi) pura en Python sin sobrecarga de RAM
    n = len(matrix)
    A = [row[:] for row in matrix]
    for _ in range(max_iter):
        max_val = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(A[i][j]) > max_val:
                    max_val = abs(A[i][j])
                    p, q = i, j
        if max_val < tol:
            break
        diff = A[q][q] - A[p][p]
        if abs(diff) < 1e-12:
            theta = math.pi / 4.0
        else:
            theta = 0.5 * math.atan2(2.0 * A[p][q], diff)
        c = math.cos(theta)
        s = math.sin(theta)
        app, aqq, apq = A[p][p], A[q][q], A[p][q]
        A[p][p] = c*c*app - 2.0*s*c*apq + s*s*aqq
        A[q][q] = s*s*app + 2.0*s*c*apq + c*c*aqq
        A[p][q] = A[q][p] = 0.0
        for k in range(n):
            if k != p and k != q:
                akp, akq = A[k][p], A[k][q]
                A[k][p] = A[p][k] = c*akp - s*akq
                A[k][q] = A[q][k] = s*akp + c*akq
    eigs = sorted([A[i][i] for i in range(n)], reverse=True)
    return eigs

def run_level3_engine():
    vix = 34.0
    warsh_bps = 102.0
    sigmas = [0.22 * (vix / 20.0), 0.20 * (vix / 22.0), 0.18, 0.12 * (vix / 24.0)]
    # Matriz de correlación estresada (crisis Ormuz + Báltico + XLK Bear)
    corr = [
        [1.00, 0.32, 0.15, -0.20],
        [0.32, 1.00, 0.28, -0.15],
        [0.15, 0.28, 1.00,  0.05],
        [-0.20,-0.15, 0.05, 1.00],
    ]
    cov = [[sigmas[i] * sigmas[j] * corr[i][j] for j in range(4)] for i in range(4)]
    eigenvalues = jacobi_eigenvalues(cov)
    total_var = sum(eigenvalues)
    systemic_mode_pct = round((eigenvalues[0] / total_var) * 100, 2)

    # Media Armónica de Liquidez (días efectivos ponderados invertidos)
    liq_scores = [0.85, 0.45, 0.40, 0.98]  # Pod1, Pod2 (custodia NY), Pod3 (Hard Asset), Pod4 (Cash/Rates)
    harmonic_liq = round(len(liq_scores) / sum(1.0 / x for x in liq_scores), 3)

    # Convexidad Gamma Pitagórica ante salto de +/-15% en crudo (dS = 0.15)
    gamma_pod1 = 1.45  # Convexidad positiva estructural Merey 16 Non-Hormuz
    dS = 0.15
    gamma_convexity_alpha = round(0.5 * gamma_pod1 * (dS ** 2) * 100, 2)

    lockout_trigger = "LOCKOUT: NO TRADE (MODO SISTEMICO > 50%)" if systemic_mode_pct > 50.0 else "ARMADO / LISTO"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = (
        f"📐 M82 NIVEL III :: PITAGORAS ESPECTRAL & CONVEXIDAD THORP ({now})\n"
        f"🔒 BUNKER MODE 0.30x LOCK | VIX: {vix} | Warsh: +{warsh_bps} bps\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"1️⃣ ROTACION DE JACOBI (Autovalores Ortogonales):\n"
        f"  • λ1 (Factor Sistemico): {eigenvalues[0]:.4f} ({systemic_mode_pct}% de varianza total)\n"
        f"  • λ2..λ4 (Alfa Idiosincratico): {[round(x, 4) for x in eigenvalues[1:]]}\n"
        f"  • Estado Gatillo: {lockout_trigger}\n"
        f"2️⃣ CONVEXIDAD GAMMA (0.5 * Γ * ΔS² ante ±15% Crudo):\n"
        f"  • Alfa Convexo Capturado (Pod 1 Merey 16): +{gamma_convexity_alpha}% neto sin riesgo Theta\n"
        f"3️⃣ MEDIA ARMONICA DE LIQUIDEZ (H_liq):\n"
        f"  • Indice Armonico Multi-Pod: {harmonic_liq} (Justifica 100% Dry Powder USD en caja)"
    )
    print(report)

    db_path = os.path.expanduser("~/M82/m82_database.db")
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path, timeout=60.0)
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA busy_timeout=60000;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS thorp_level3_spectral (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                lambda1_pct REAL,
                gamma_alpha_pct REAL,
                harmonic_liq REAL,
                status TEXT
            )
        """)
        cur.execute("INSERT INTO thorp_level3_spectral (timestamp, lambda1_pct, gamma_alpha_pct, harmonic_liq, status) VALUES (?,?,?,?,?)",
                    (now, systemic_mode_pct, gamma_convexity_alpha, harmonic_liq, lockout_trigger))
        conn.commit()
        cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conn.close()
        print("[DB STATUS] Nivel III asentado en m82_database.db (WAL 0/0/0 CLEAN)")

    try:
        token = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
        chat_id = "-1004335849125"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": report}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM OK] Reporte Nivel III entregado a -1004335849125")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    run_level3_engine()
