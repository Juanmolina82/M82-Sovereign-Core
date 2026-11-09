import pathlib, os

p = pathlib.Path.home() / "M82" / "m82_dossier.py"
if not p.exists():
    # Fallback si el script principal es un ejecutable m82 directo
    p = pathlib.Path.home() / "M82" / "m82"

t = p.read_text()

futures_block = '''
# --- FUTUROS GLOBALES (RIC) - Vector Proxy de Estructura / Cobertura ---
FUTURES_PRESETS = {
    "CLc1":  {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 74.20, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "LCOc1": {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 78.45, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "NGc1":  {"name": "Natural Gas Future", "sector": "ENERGY / FUTURES", "spot": 2.68, "fcf": 3.20, "ev": 0.0, "pe": 0.0, "rsi": 42.0, "stoch": 38.0, "rel": 0.0, "short": 0.0, "val_a": 3.20},
    "RBc1":  {"name": "RBOB Gasoline", "sector": "ENERGY / FUTURES", "spot": 2.15, "fcf": 3.80, "ev": 0.0, "pe": 0.0, "rsi": 46.0, "stoch": 44.0, "rel": 0.0, "short": 0.0, "val_a": 3.80},
    "HOc1":  {"name": "Heating Oil", "sector": "ENERGY / FUTURES", "spot": 2.32, "fcf": 3.80, "ev": 0.0, "pe": 0.0, "rsi": 46.0, "stoch": 44.0, "rel": 0.0, "short": 0.0, "val_a": 3.80},
    "GCc1":  {"name": "Gold Future", "sector": "METALS / FUTURES", "spot": 2738.50, "fcf": 7.79, "ev": 0.0, "pe": 0.0, "rsi": 55.0, "stoch": 52.0, "rel": 0.0, "short": 0.0, "val_a": 7.79},
    "SIc1":  {"name": "Silver Future", "sector": "METALS / FUTURES", "spot": 32.40, "fcf": 5.20, "ev": 0.0, "pe": 0.0, "rsi": 52.0, "stoch": 50.0, "rel": 0.0, "short": 0.0, "val_a": 5.20},
    "HGc1":  {"name": "Copper Future", "sector": "METALS / FUTURES", "spot": 4.35, "fcf": 5.80, "ev": 0.0, "pe": 0.0, "rsi": 54.0, "stoch": 51.0, "rel": 0.0, "short": 0.0, "val_a": 5.80},
    "ESc1":  {"name": "S&P 500 Future", "sector": "INDEX / FUTURES", "spot": 5780.25, "fcf": 3.50, "ev": 0.0, "pe": 0.0, "rsi": 50.0, "stoch": 48.0, "rel": 0.0, "short": 0.0, "val_a": 3.50},
    "NQc1":  {"name": "Nasdaq 100 Future", "sector": "INDEX / FUTURES", "spot": 20420.50, "fcf": 3.80, "ev": 0.0, "pe": 0.0, "rsi": 51.0, "stoch": 49.0, "rel": 0.0, "short": 0.0, "val_a": 3.80},
    "VXc1":  {"name": "VIX Future", "sector": "VOLATILITY / FUTURES", "spot": 15.80, "fcf": 2.00, "ev": 0.0, "pe": 0.0, "rsi": 35.0, "stoch": 28.0, "rel": 0.0, "short": 0.0, "val_a": 2.00},
    "ZCc1":  {"name": "Corn Future", "sector": "AGRI / FUTURES", "spot": 412.50, "fcf": 3.00, "ev": 0.0, "pe": 0.0, "rsi": 44.0, "stoch": 42.0, "rel": 0.0, "short": 0.0, "val_a": 3.00},
    "ZSc1":  {"name": "Soybean Future", "sector": "AGRI / FUTURES", "spot": 998.25, "fcf": 3.10, "ev": 0.0, "pe": 0.0, "rsi": 45.0, "stoch": 43.0, "rel": 0.0, "short": 0.0, "val_a": 3.10},
}
'''

if "FUTURES_PRESETS" not in t:
    if "PRESETS = {" in t:
        t = t.replace("PRESETS = {", futures_block + "\nPRESETS = {", 1)
    else:
        t = futures_block + "\n" + t
        
    if "if d is None:" in t:
        t = t.replace(
            "if d is None:",
            "if d is None:\n        _f = FUTURES_PRESETS.get(ticker)\n        if _f is not None:\n            d = dict(_f)\n            print(f'[M82 FUTURES] Contrato de Futuros {ticker} — {_f[\"name\"]}')\n    if d is None:"
        )
    p.write_text(t)
    print("[PATCH FUTURES OK] m82 ahora resuelve CLc1, GCc1, ESc1, etc.")
else:
    print("[PATCH] FUTURES_PRESETS ya existe en la arquitectura.")
