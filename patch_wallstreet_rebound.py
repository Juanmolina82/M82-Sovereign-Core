import os, json, time
DATA_PATH = os.path.expanduser("~/M82/app/data.json")
payload = {}
if os.path.exists(DATA_PATH):
    try:
        with open(DATA_PATH) as f: payload = json.load(f)
    except Exception: payload = {}

patch = {
    "wire": "M82 WIRE: USA-STOCKS UPDATE 1 - Wall Street Rebound tras AI Selloff - NVDA sigue en rojo | 9 Nov 2026",
    "timestamp": time.strftime("%H:%M:%S VET"),
    "audit_source": "LSEG Reuters USA-STOCKS UPDATE 1 - Version China",
    "wallstreet_open": {
        "dow": "+1.27% - 51,938.22 (+652.49)",
        "sp500": "+1.48% - 7,485.67 (+108.81)",
        "nasdaq": "+1.87% - 25,038.34 (+458.92)",
        "breadth_nyse": "3.87:1 al alza",
        "breadth_nasdaq": "2.32:1 al alza",
        "sectors_up": "9 de 11 - Lideran Consumo Discrecional y Comunicacion"
    },
    "nvda_update": "NVDA -5.6% en este cable (vs -8% apertura UPDATE 6) - Investigacion Huang sigue pesando",
    "chips_rebound": {
        "sox": "+3.3% - peor semana desde Mar 2025 revertida parcial",
        "marvell": "+5%",
        "broadcom": "+6.5%",
        "intel": "+2%",
        "qualcomm": "+2%",
        "mega_caps": "MSFT / GOOGL / META / AMZN +2.5% a +5% - TSLA +4.5%"
    },
    "thesis_update": "Morgan Stanley + UBS: Caida AI semana pasada fue SOBRE-REACCION - Riesgo regulacion extrema Data Centers con Congreso democrata POCO PROBABLE - Debilita Cadena Midterms",
    "next_catalyst": "CPI Martes - Expectativa Reuters +2.7% YoY - Si sale alto, vuelve miedo hike Dic (FedWatch 79%)",
    "earnings": "335 empresas S&P reportadas - 82.4% supero expectativas - KKR +1% profit record - CEG +2.8% - BRK.B -0.1%",
    "risk": "BUNKER MODE / 0.30x LOCK - 100% Dry Powder - 0 ejecuciones - NO CAMBIA POSTURA"
}
payload.update(patch)
tmp = DATA_PATH + ".tmp"
with open(tmp, "w") as f: json.dump(payload, f, indent=2)
os.replace(tmp, DATA_PATH)
print("[SYNC OK] Wall Street Rebound sellado en CORE.")
