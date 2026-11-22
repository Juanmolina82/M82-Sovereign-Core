import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

import sqlite3, math, datetime, urllib.request, urllib.parse

M82_DIR = os.path.expanduser("~/M82")
QUANT_DB = os.path.join(M82_DIR, "m82_quant_engine.db")
DOC_OUT = os.path.join(M82_DIR, "docs", "M82_SUNDAY_PREFLIGHT_BRIEF.md")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TG_CHAT = "-1004335849125"

def invert_4x4(M):
    # Inversión matricial Gauss-Jordan pura en Python (cero dependencia NumPy/RAM)
    n = 4
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for i in range(n):
        pivot = A[i][i]
        if abs(pivot) < 1e-12:
            pivot = 1e-12
        for j in range(2 * n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(2 * n):
                    A[k][j] -= factor * A[i][j]
    return [row[n:] for row in A]

def run_level7_frontier():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")
    rf, warsh_spread, vix = 0.0435, 0.0102, 34.0
    hurdle = rf + warsh_spread
    bunker_cap = 0.30
    active_exp = 0.22

    names = ["POD1_MEREY16_CRACK", "POD2_SOVEREIGN_OFAC", "POD3_GAS_COMPUTE_010", "POD4_RATES_FX_SHIELD"]
    mus = [0.195, 0.175, 0.230, 0.125]
    sigmas = [0.22 * (vix / 20.0), 0.20 * (vix / 22.0), 0.18, 0.12 * (vix / 24.0)]
    corr = [
        [1.00, 0.32, 0.15, -0.20],
        [0.32, 1.00, 0.28, -0.15],
        [0.15, 0.28, 1.00,  0.05],
        [-0.20,-0.15, 0.05, 1.00],
    ]
    cov = [[sigmas[i] * sigmas[j] * corr[i][j] for j in range(4)] for i in range(4)]
    inv_cov = invert_4x4(cov)
    excess = [m - hurdle for m in mus]

    # w_raw = Sigma^-1 * (mu - hurdle)
    w_raw = [max(0.0, sum(inv_cov[i][j] * excess[j] for j in range(4))) for i in range(4)]
    w_sum = sum(w_raw) or 1.0
    w_opt = [round(w / w_sum, 4) for w in w_raw]

    # Métricas de la Frontera Óptima bajo exposición activa 0.22x
    mu_port = sum(w_opt[i] * mus[i] for i in range(4))
    var_port = sum(w_opt[i] * w_opt[j] * cov[i][j] for i in range(4) for j in range(4))
    sigma_opt = math.sqrt(var_port)
    sharpe_opt = round((mu_port - hurdle) / sigma_opt, 2)
    var99_opt = round((sigma_opt / math.sqrt(252.0)) * 2.326 * active_exp * 100, 2)

    alloc_lines = []
    for i in range(4):
        eff_alloc = round(w_opt[i] * active_exp * 100, 2)
        alloc_lines.append(f"  • {names[i]}: Peso Óptimo {w_opt[i]*100:.1f}% → Asignación Real: {eff_alloc}% capital")

    preflight_status = "LOCKOUT: NO TRADE (VIX 34.0 > 28.0 | ESPERAR APERTURA 18:00 VET)"

    # Persistir en base analítica dedicada (Zero-Contention)
    conn = sqlite3.connect(QUANT_DB, timeout=60.0)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("""CREATE TABLE IF NOT EXISTS m82_dynamic_frontier_l7 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, sharpe_opt REAL, sigma_opt_pct REAL, var99_opt_pct REAL,
        w_pod1 REAL, w_pod2 REAL, w_pod3 REAL, w_pod4 REAL, status TEXT
    )""")
    cur.execute("INSERT INTO m82_dynamic_frontier_l7 (timestamp, sharpe_opt, sigma_opt_pct, var99_opt_pct, w_pod1, w_pod2, w_pod3, w_pod4, status) VALUES (?,?,?,?,?,?,?,?,?)",
                (now, sharpe_opt, round(sigma_opt*100, 2), var99_opt, w_opt[0], w_opt[1], w_opt[2], w_opt[3], preflight_status))
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    # Exportar Briefing Markdown para MM82 (NotebookLM) & GitHub Vault
    brief_md = (
        f"# M82 SUNDAY PRE-FLIGHT BRIEFING :: FRONTERA DINÁMICA NIVEL VII\n"
        f"**Timestamp:** {now} | **Nodo:** Charallave L4/L5 Edge $\\otimes$ Caracas HQ\n"
        f"**Gobernanza:** `BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK` | **Estado:** `{preflight_status}`\n\n"
        f"## 1. Asignación Óptima Markowitz–Thorp (Sharpe Pitagórico: `{sharpe_opt}`)\n"
        f"* **Volatilidad Óptima Multi-Pod:** `{sigma_opt*100:.2f}%` | **VaR 99% Diario (Exp. 0.22x):** `{var99_opt}%`\n"
        + "\n".join(alloc_lines) + "\n\n"
        f"## 2. Protocolo de Apertura Dominical (18:00 VET)\n"
        f"* **Vector Energía Non-Hormuz:** Monitorear diferencial *Merey 16 / Brent* tras cierre del Estrecho de Ormuz (*Khat Shekan*) y ataques en Bahréin.\n"
        f"* **Vector Norte / Ciber:** Vigilar apertura de futuros europeos tras incidente *Sparta II* (Finlandia) y DDoS `ID-porten` (Noruega).\n"
        f"* **Regla de Desbloqueo:** Mantener `100% Dry Powder USD` en custodia federal hasta que `VIX < 28.0` y $\\lambda_1 < 50\\%$.\n"
    )
    os.makedirs(os.path.dirname(DOC_OUT), exist_ok=True)
    with open(DOC_OUT, "w", encoding="utf-8") as f:
        f.write(brief_md)

    tg_msg = (
        f"🧭 M82 NIVEL VII :: FRONTERA DINÁMICA & PRE-FLIGHT APERTURA ({now})\n"
        f"🔒 BUNKER 0.30x LOCK | Exp. Activa: {active_exp}x | Sharpe Óptimo: {sharpe_opt}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 ASIGNACIÓN ÓPTIMA MARKOWITZ–THORP:\n"
        + "\n".join(alloc_lines) + "\n"
        f"🛡️ VaR 99% Diario Optimizado: {var99_opt}% (Vol. Óptima: {sigma_opt*100:.2f}%)\n"
        f"🚦 Gatillo Apertura: {preflight_status}\n"
        f"📄 Briefing sellado en docs/M82_SUNDAY_PREFLIGHT_BRIEF.md"
    )
    print(tg_msg)
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": tg_msg}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM OK] Reporte Nivel VII entregado a -1004335849125")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    run_level7_frontier()
