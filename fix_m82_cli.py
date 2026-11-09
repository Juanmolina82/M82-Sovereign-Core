import os, sys, pathlib

# Localizar el ejecutable m82 real en el sistema
possible_paths = [
    pathlib.Path.home() / "M82" / "m82",
    pathlib.Path.home() / "M82" / "m82_dossier.py",
    pathlib.Path("/data/data/com.termux/files/usr/bin/m82"),
]

futures_tickers = "['CLc1', 'LCOc1', 'NGc1', 'RBc1', 'HOc1', 'GCc1', 'SIc1', 'HGc1', 'ESc1', 'NQc1', 'VXc1', 'ZCc1', 'ZSc1']"

for target in possible_paths:
    if target.exists() and target.is_file():
        try:
            content = target.read_text()
            modified = False
            
            # 1. Liberar la guardia de validación de tickers
            if "TICKERS_DISPONIBLES" in content and "CLc1" not in content:
                content = content.replace(
                    "TICKERS_DISPONIBLES =",
                    f"TICKERS_DISPONIBLES = {futures_tickers} +"
                )
                modified = True

            # 2. Inyectar fallback directo a BBDD o Futuros si no existe en PRESETS
            if "PRESETS.get(ticker)" in content and "FUTURES_PRESETS" not in content:
                futures_preset_code = """
FUTURES_PRESETS = {
    "CLc1":  {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 74.20, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "LCOc1": {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 78.45, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "GCc1":  {"name": "Gold Future", "sector": "METALS / FUTURES", "spot": 2738.50, "fcf": 7.79, "ev": 0.0, "pe": 0.0, "rsi": 55.0, "stoch": 52.0, "rel": 0.0, "short": 0.0, "val_a": 7.79},
    "ESc1":  {"name": "S&P 500 Future", "sector": "INDEX / FUTURES", "spot": 5780.25, "fcf": 3.50, "ev": 0.0, "pe": 0.0, "rsi": 50.0, "stoch": 48.0, "rel": 0.0, "short": 0.0, "val_a": 3.50},
    "VXc1":  {"name": "VIX Future", "sector": "VOLATILITY / FUTURES", "spot": 15.80, "fcf": 2.00, "ev": 0.0, "pe": 0.0, "rsi": 35.0, "stoch": 28.0, "rel": 0.0, "short": 0.0, "val_a": 2.00},
}
"""
                content = content.replace("PRESETS = {", futures_preset_code + "\nPRESETS = {")
                content = content.replace("PRESETS.get(ticker)", "(PRESETS.get(ticker) or FUTURES_PRESETS.get(ticker))")
                modified = True

            if modified:
                target.write_text(content)
                print(f"[HOTFIX OK] Parcheado exitosamente: {target}")
        except Exception as e:
            print(f"[HOTFIX WARN] Error procesando {target}: {e}")

