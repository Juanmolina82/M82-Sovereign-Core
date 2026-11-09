import pathlib, re

futures_list = "['CLc1', 'LCOc1', 'NGc1', 'RBc1', 'HOc1', 'GCc1', 'SIc1', 'HGc1', 'ESc1', 'NQc1', 'VXc1', 'ZCc1', 'ZSc1']"

futures_presets_dict = """
    "CLc1":  {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 74.20, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "LCOc1": {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 78.45, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "GCc1":  {"name": "Gold Future", "sector": "METALS / FUTURES", "spot": 2738.50, "fcf": 7.79, "ev": 0.0, "pe": 0.0, "rsi": 55.0, "stoch": 52.0, "rel": 0.0, "short": 0.0, "val_a": 7.79},
    "ESc1":  {"name": "S&P 500 Future", "sector": "INDEX / FUTURES", "spot": 5780.25, "fcf": 3.50, "ev": 0.0, "pe": 0.0, "rsi": 50.0, "stoch": 48.0, "rel": 0.0, "short": 0.0, "val_a": 3.50},
    "VXc1":  {"name": "VIX Future", "sector": "VOLATILITY / FUTURES", "spot": 15.80, "fcf": 2.00, "ev": 0.0, "pe": 0.0, "rsi": 35.0, "stoch": 28.0, "rel": 0.0, "short": 0.0, "val_a": 2.00},
"""

# Archivos clave identificados en el ls -la de su pantalla
target_files = [
    "m82", "m82_dossier.py", "m82_master_dossier.py", 
    "m82_core_engine.py", "patch_presets.sh"
]

for filename in target_files:
    path = pathlib.Path.home() / "M82" / filename
    if path.exists():
        content = path.read_text()
        modified = False
        
        # 1. Liberar la guardia TICKERS_DISPONIBLES
        if "TICKERS_DISPONIBLES" in content and "CLc1" not in content:
            content = content.replace("TICKERS_DISPONIBLES = [", f"TICKERS_DISPONIBLES = {futures_list} + [")
            modified = True
            
        # 2. Inyectar en diccionarios de presets
        if "PRESETS = {" in content and '"CLc1"' not in content:
            content = content.replace("PRESETS = {", "PRESETS = {\n" + futures_presets_dict)
            modified = True

        if modified:
            path.write_text(content)
            print(f"[CORE PATCH OK] Inyectados derivados en: {filename}")

