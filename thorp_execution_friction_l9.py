import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

import sqlite3, math, datetime, urllib.request, urllib.parse

M82_DIR = os.path.expanduser("~/M82")
QUANT_DB = os.path.join(M82_DIR, "m82_quant_engine.db")
X_POST_FILE = os.path.join(M82_DIR, "logs", "x_post_latest.txt")
TG_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
TG_CHAT = "-1004335849125"

os.makedirs(os.path.dirname(X_POST_FILE), exist_ok=True)

def run_level9_friction():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")
    rf = 0.0435
    warsh_spread = 0.0102
    vix = 34.0
    active_exp = 0.22

    # (Nombre, mu_bruto, sigma_estresada, spread_bps, demurrage_bps, q_over_v, peso_optimo_l7)
    pods_l9 = [
        ("POD1_MEREY16_CRACK",   0.195, 0.22 * (vix / 20.0), 35.0, 15.0, 0.0040, 0.0915),
        ("POD2_SOVEREIGN_OFAC",  0.175, 0.20 * (vix / 22.0), 65.0,  0.0, 0.0025, 0.0440),
        ("POD3_GAS_COMPUTE_010", 0.230, 0.18,                15.0,  0.0, 0.0010, 0.5593),
        ("POD4_RATES_FX_SHIELD", 0.125, 0.12 * (vix / 24.0), 12.0,  0.0, 0.0015, 0.3053),
    ]

    lines = []
    net_port_alpha = 0.0
    total_friction_bps = 0.0

    for name, mu, sigma, spread_bps, dem_bps, q_v, w_opt in pods_l9:
        impact_pct = 0.5 * sigma * math.sqrt(q_v)
        spread_pct = (spread_bps + dem_bps) / 10000.0
        total_cost = rf + warsh_spread + spread_pct + impact_pct
        mu_net = mu - total_cost
        net_port_alpha += w_opt * mu_net
        total_friction_bps += w_opt * (spread_bps + dem_bps + impact_pct * 10000.0)
        extra_tag = f"+Demurrage {int(dem_bps)}bps" if dem_bps > 0 else ""
        lines.append(
            f"  • {name}: Neto={mu_net*100:.2f}% | √(Q/V)={impact_pct*100:.2f}% | Spread={int(spread_bps)}bps {extra_tag}".strip()
        )

    net_port_alpha_pct = round(net_port_alpha * 100, 2)
    avg_friction_bps = round(total_friction_bps, 1)
    no_trade_band_pct = round(2.5 * (vix / 20.0), 2)
    exec_verdict = "HOLD / BANDA ±4.25% ACTIVA (DEMURRAGE PADD 3 CONTENIDO)"

    x_post = "Ciberofensiva sobre Corpus Christi (PADD 3) y puertos de EE.UU. eleva riesgo de demurrage y volatilidad en Crack Spreads. En M82 aplicamos fricción Nivel IX (35 bps + banda ±4.25%) bajo BUNKER 0.30x LOCK. Dry Powder blindado. #Energy #Macro #M82"
    with open(X_POST_FILE, "w", encoding="utf-8") as f:
        f.write(x_post + "\n")

    conn = sqlite3.connect(QUANT_DB, timeout=60.0)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("""CREATE TABLE IF NOT EXISTS m82_execution_friction_l9 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT, net_alpha_pct REAL, avg_friction_bps REAL,
        no_trade_band_pct REAL, verdict TEXT
    )""")
    cur.execute("INSERT INTO m82_execution_friction_l9 (timestamp, net_alpha_pct, avg_friction_bps, no_trade_band_pct, verdict) VALUES (?,?,?,?,?)",
                (now, net_port_alpha_pct, avg_friction_bps, no_trade_band_pct, exec_verdict))
    conn.commit()
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.close()

    msg = (
        f"⚙️ M82 NIVEL IX :: FRICCIÓN PADD 3 / DEMURRAGE & IMPACTO PITAGÓRICO ({now})\n"
        f"🔒 BUNKER 0.30x LOCK | Exp. Activa: {active_exp}x | VIX: {vix}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📉 AUDITORÍA DE COSTOS REALES (Beat the Market - Thorp):\n"
        + "\n".join(lines) + "\n"
        f"📊 SÍNTESIS POST-FRICCIÓN:\n"
        f"  • Alfa Neto Ponderado: +{net_port_alpha_pct}% | Fricción Media: {avg_friction_bps} bps\n"
        f"  • Banda No-Trade Thorp: ±{no_trade_band_pct}% | Veredicto: {exec_verdict}\n"
        f"🐦 X DRAFT ({len(x_post)} chars): {x_post}"
    )
    print(msg)
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TG_CHAT, "text": msg}).encode("utf-8")
        urllib.request.urlopen(url, data=data, timeout=10)
        print("[TELEGRAM OK] Reporte Nivel IX + X Post entregado a -1004335849125")
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")

if __name__ == "__main__":
    run_level9_friction()
