import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import sqlite3, math, datetime, urllib.request, urllib.parse, json

def run_pythagoras_thorp_matrix():
    rf = 0.0435             # Tasa libre de riesgo USD
    warsh_spread = 0.0102   # +102.0 bps
    vix = 34.0              # Shock volatilidad CBOE
    bunker_cap = 0.30       # BUNKER MODE 0.30x LOCK
    kelly_lambda = 0.25     # Fractional Kelly conservador (Thorp)

    # Definición de los 4 Pods Ortogonales M82: (nombre, mu_anual, sigma_base, peso_objetivo)
    pods = [
        ("POD1_MEREY16_CRACK",   0.195, 0.22 * (vix / 20.0), 0.35),
        ("POD2_SOVEREIGN_OFAC",  0.175, 0.20 * (vix / 22.0), 0.25),
        ("POD3_GAS_COMPUTE_010", 0.230, 0.18,                0.25),
        ("POD4_RATES_FX_SHIELD", 0.125, 0.12 * (vix / 24.0), 0.15),
    ]

    # Matriz de correlaciones bajas (ortogonalidad pitagórica entre Pods)
    corr = [
        [1.00, 0.18, 0.10, -0.15],
        [0.18, 1.00, 0.22, -0.10],
        [0.10, 0.22, 1.00,  0.05],
        [-0.15,-0.10, 0.05, 1.00],
    ]

    results = []
    var_sum_sq = 0.0
    var_linear_sum = 0.0

    for i, (name, mu, sigma, w) in enumerate(pods):
        excess_ret = mu - (rf + warsh_spread)
        f_star = max(0.0, excess_ret / (sigma ** 2))
        f_m82 = round(min(kelly_lambda * f_star, bunker_cap), 4)
        results.append((name, f_star, f_m82, sigma, w))
        var_linear_sum += w * sigma

    # Varianza Pitagórica Multi-Pod: sqrt(w^T * Sigma * w)
    for i in range(len(pods)):
        for j in range(len(pods)):
            wi, si = pods[i][3], pods[i][2]
            wj, sj = pods[j][3], pods[j][2]
            var_sum_sq += wi * wj * si * sj * corr[i][j]

    sigma_portfolio = math.sqrt(var_sum_sq)
    diversification_benefit_pct = round((1.0 - (sigma_portfolio / var_linear_sum)) * 100, 2)
    active_exposure = 0.22  # Exposición activa actual bajo BUNKER MODE 0.30x LOCK
    daily_var_99 = round((sigma_portfolio / math.sqrt(252)) * 2.326 * active_exposure * 100, 2)

    lines = [
        f"M82 PYTHAGORAS-THORP MATRIX ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
        f"Regimen: VIX={vix} | Warsh={warsh_spread*10000:.1f}bps | BUNKER 0.30x LOCK (Activa: {active_exposure}x)",
        f"Volatilidad Lineal: {var_linear_sum*100:.2f}% -> Pitagorica Multi-Pod: {sigma_portfolio*100:.2f}% (Reduccion Riesgo: -{diversification_benefit_pct}%)",
        f"VaR Diario 99% Estimado: {daily_var_99}% (Target M82: ~1.68%)"
    ]
    for name, f_star, f_m82, sigma, w in results:
        lines.append(f"• {name}: Kelly Puro={f_star:.2f}x | M82 Fraccional={f_m82:.2f}x (Peso {int(w*100)}%)")

    report = "\n".join(lines)
    print(report)

    # Persistencia en SQLite3 WAL Mode
    db_path = os.path.expanduser("~/M82/m82_database.db")
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path, timeout=60.0)
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA busy_timeout=60000;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS thorp_matrix_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                sigma_linear REAL,
                sigma_pythagoras REAL,
                risk_reduction_pct REAL,
                daily_var_99_pct REAL,
                vix REAL
            )
        """)
        now = datetime.datetime.utcnow().isoformat()
        cur.execute("INSERT INTO thorp_matrix_runs (timestamp, sigma_linear, sigma_pythagoras, risk_reduction_pct, daily_var_99_pct, vix) VALUES (?,?,?,?,?,?)",
                    (now, round(var_linear_sum, 4), round(sigma_portfolio, 4), diversification_benefit_pct, daily_var_99, vix))
        conn.commit()
        cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conn.close()
        print("[DB STATUS] Sellado en m82_database.db -> thorp_matrix_runs (WAL 0/0/0 CLEAN)")

    # Despacho a Telegram
    try:
        token = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
        chat_id = "-1004335849125"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": report}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM] Reporte matricial entregado a -1004335849125")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    run_pythagoras_thorp_matrix()
