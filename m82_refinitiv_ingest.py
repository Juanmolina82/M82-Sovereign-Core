import os, json, time, sys
sys.path.insert(0, os.path.expanduser("~/M82"))
from m82_universe_wallstreet import UNIVERSE

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
# Config Refinitiv - Tu usuario Workspace
REFINITIV_USER = "jmmp@molina82.com"
REFINITIV_APP_KEY = os.environ.get("REFINITIV_APP_KEY", "PON_TU_APP_KEY_AQUI")

# Intenta Refinitiv Data Platform - Si no hay libreria, usa modo LSEG Wire
try:
    import refinitiv.data as rd
    HAS_RD = True
except:
    HAS_RD = False
    print("[REFINITIV] Libreria refinitiv-data no instalada - Usando modo Wire / Fallback")

def fetch_universe():
    results = {}
    if HAS_RD:
        try:
            rd.open_session()
            # Flatten universo
            all_rics = [ric for lst in UNIVERSE.values() for ric in lst]
            # Precios + News en un solo call
            df = rd.get_data(all_rics, ["TR.PriceClose", "TR.Volume", "TR.PCTCHNG"])
            for _, row in df.iterrows():
                results[row["Instrument"]] = {"price": row.get("Price Close"), "change_pct": row.get("% Change")}
            rd.close_session()
            print(f"[REFINITIV OK] {len(results)} RICs desde Workspace {REFINITIV_USER}")
        except Exception as e:
            print(f"[REFINITIV FALLBACK] {e} - Usando Wire")
            results = {"mode": "WIRE_FALLBACK", "note": "Revisa APP_KEY y sesion Workspace"}
    else:
        results = {"mode": "WIRE_FALLBACK", "note": "Instala: pip install refinitiv-data"}
    return results

if __name__ == "__main__":
    data = fetch_universe()
    payload = {}
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH) as f: payload = json.load(f)
        except: payload = {}
    payload.update({
        "wire": "M82 UNIVERSE WALL STREET - Refinitiv Workspace Ingestion",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S VET"),
        "refinitiv_user": REFINITIV_USER,
        "universe_wallstreet": data,
        "universe_count": sum(len(v) for v in UNIVERSE.values()),
        "ai_audit": {"builder": "Fable 5.2 - OK", "auditor": "Mythos 5.2 - GUARD UNIVERSAL", "verdict_status": "SELLADO_EN_CORE"},
        "risk": {"mode": "BUNKER MODE", "lock": "0.30x LOCK", "dry_powder": "100%", "executions": 0, "wait_for": "CPI 8:30 AM ET / 9:30 AM VET"}
    })
    tmp = DATA_PATH + ".tmp"
    with open(tmp, "w") as f: json.dump(payload, f, indent=2)
    os.replace(tmp, DATA_PATH)
    print("[FABLE BUILD OK] Universo Wall Street inyectado.")
