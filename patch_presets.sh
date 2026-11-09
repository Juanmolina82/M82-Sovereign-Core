#!/usr/bin/env bash
cd ~/M82 || exit 1

python3 - << 'PYEOF'
import pathlib

p = pathlib.Path("m82_dossier.py")
txt = p.read_text()

# Inyección de presets ampliados para Wall Street, ETFs y Crypto
presets_code = """    PRESETS = {

    "CLc1":  {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 74.20, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "LCOc1": {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 78.45, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "GCc1":  {"name": "Gold Future", "sector": "METALS / FUTURES", "spot": 2738.50, "fcf": 7.79, "ev": 0.0, "pe": 0.0, "rsi": 55.0, "stoch": 52.0, "rel": 0.0, "short": 0.0, "val_a": 7.79},
    "ESc1":  {"name": "S&P 500 Future", "sector": "INDEX / FUTURES", "spot": 5780.25, "fcf": 3.50, "ev": 0.0, "pe": 0.0, "rsi": 50.0, "stoch": 48.0, "rel": 0.0, "short": 0.0, "val_a": 3.50},
    "VXc1":  {"name": "VIX Future", "sector": "VOLATILITY / FUTURES", "spot": 15.80, "fcf": 2.00, "ev": 0.0, "pe": 0.0, "rsi": 35.0, "stoch": 28.0, "rel": 0.0, "short": 0.0, "val_a": 2.00},

        "DELL.N": {"name": "Dell Technologies", "spot": 123.05, "fcf": 8.25, "ev_ebitda": 7.21, "fwd_pe": 12.75, "rsi": 32.50, "stoch": 18.40, "rel_pe": 0.56, "short": 1.66, "val_a": 8.25, "verdict": "COMPRA / ACUMULACION FUERTE [VERDE]"},
        "NVDA": {"name": "Nvidia Corp", "spot": 165.00, "fcf": 4.20, "ev_ebitda": 28.50, "fwd_pe": 24.10, "rsi": 48.00, "stoch": 45.00, "rel_pe": 1.25, "short": 1.10, "val_a": 4.20, "verdict": "ESPERA / ACUMULACION SELECTIVA [NEUTRO]"},
        "AAPL": {"name": "Apple Inc", "spot": 224.50, "fcf": 3.80, "ev_ebitda": 22.10, "fwd_pe": 28.40, "rsi": 52.10, "stoch": 55.00, "rel_pe": 1.15, "short": 0.85, "val_a": 3.80, "verdict": "NEUTRO / HOLD [AMARILLO]"},
        "MSFT": {"name": "Microsoft Corp", "spot": 415.20, "fcf": 3.40, "ev_ebitda": 21.50, "fwd_pe": 31.20, "rsi": 49.30, "stoch": 42.00, "rel_pe": 1.10, "short": 0.72, "val_a": 3.40, "verdict": "ESPERA / ACUMULACION TACTICA [NEUTRO]"},
        "XLK": {"name": "Tech Select Sector SPDR", "spot": 228.40, "fcf": 3.10, "ev_ebitda": 19.80, "fwd_pe": 26.50, "rsi": 50.20, "stoch": 48.00, "rel_pe": 1.00, "short": 0.50, "val_a": 3.10, "verdict": "ACUMULACION SECTORIAL [NEUTRO]"},
        "SMH": {"name": "VanEck Semiconductor ETF", "spot": 242.10, "fcf": 3.90, "ev_ebitda": 24.20, "fwd_pe": 25.80, "rsi": 46.50, "stoch": 41.00, "rel_pe": 1.20, "short": 1.30, "val_a": 3.90, "verdict": "ESPERA / PISO TECNICO [NEUTRO]"},
        "XLE": {"name": "Energy Select Sector SPDR", "spot": 88.60, "fcf": 7.40, "ev_ebitda": 6.80, "fwd_pe": 11.20, "rsi": 44.10, "stoch": 38.00, "rel_pe": 0.65, "short": 1.80, "val_a": 7.40, "verdict": "COBERTURA ENERGIA / BUY [VERDE]"},
        "TLT": {"name": "iShares 20+ Year Treasury", "spot": 92.30, "fcf": 4.38, "ev_ebitda": 0.00, "fwd_pe": 0.00, "rsi": 38.20, "stoch": 28.00, "rel_pe": 0.00, "short": 2.10, "val_a": 4.38, "verdict": "RESGUARDO TASA / HOLD [NEUTRO]"},
        "XAU": {"name": "Oro Spot", "spot": 3940.00, "fcf": 0.00, "ev_ebitda": 0.00, "fwd_pe": 0.00, "rsi": 62.00, "stoch": 70.00, "rel_pe": 0.00, "short": 0.00, "val_a": 7.79, "verdict": "COBERTURA / HOLD [NEUTRO]"},
        "WTI": {"name": "Crudo WTI", "spot": 70.50, "fcf": 0.00, "ev_ebitda": 0.00, "fwd_pe": 0.00, "rsi": 45.00, "stoch": 38.00, "rel_pe": 0.00, "short": 0.00, "val_a": 2.78, "verdict": "RESGUARDO DEFENSIVO [NEUTRO]"},
        "HG": {"name": "Cobre", "spot": 4.85, "fcf": 0.00, "ev_ebitda": 0.00, "fwd_pe": 0.00, "rsi": 55.00, "stoch": 58.00, "rel_pe": 0.00, "short": 0.00, "val_a": 3.25, "verdict": "ACUMULACION INFRAESTRUCTURA [NEUTRO]"},
        "BTC": {"name": "Bitcoin Spot", "spot": 91200.00, "fcf": 0.00, "ev_ebitda": 0.00, "fwd_pe": 0.00, "rsi": 68.40, "stoch": 74.20, "rel_pe": 0.00, "short": 0.00, "val_a": 5.12, "verdict": "ASIMETRIA ALTA / HOLD [NEUTRO]"}
    }"""

if "PRESETS = {

    "CLc1":  {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 74.20, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "LCOc1": {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 78.45, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "GCc1":  {"name": "Gold Future", "sector": "METALS / FUTURES", "spot": 2738.50, "fcf": 7.79, "ev": 0.0, "pe": 0.0, "rsi": 55.0, "stoch": 52.0, "rel": 0.0, "short": 0.0, "val_a": 7.79},
    "ESc1":  {"name": "S&P 500 Future", "sector": "INDEX / FUTURES", "spot": 5780.25, "fcf": 3.50, "ev": 0.0, "pe": 0.0, "rsi": 50.0, "stoch": 48.0, "rel": 0.0, "short": 0.0, "val_a": 3.50},
    "VXc1":  {"name": "VIX Future", "sector": "VOLATILITY / FUTURES", "spot": 15.80, "fcf": 2.00, "ev": 0.0, "pe": 0.0, "rsi": 35.0, "stoch": 28.0, "rel": 0.0, "short": 0.0, "val_a": 2.00},
" in txt:
    start = txt.find("PRESETS = {

    "CLc1":  {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 74.20, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "LCOc1": {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 78.45, "fcf": 4.50, "ev": 0.0, "pe": 0.0, "rsi": 48.0, "stoch": 45.0, "rel": 0.0, "short": 0.0, "val_a": 4.50},
    "GCc1":  {"name": "Gold Future", "sector": "METALS / FUTURES", "spot": 2738.50, "fcf": 7.79, "ev": 0.0, "pe": 0.0, "rsi": 55.0, "stoch": 52.0, "rel": 0.0, "short": 0.0, "val_a": 7.79},
    "ESc1":  {"name": "S&P 500 Future", "sector": "INDEX / FUTURES", "spot": 5780.25, "fcf": 3.50, "ev": 0.0, "pe": 0.0, "rsi": 50.0, "stoch": 48.0, "rel": 0.0, "short": 0.0, "val_a": 3.50},
    "VXc1":  {"name": "VIX Future", "sector": "VOLATILITY / FUTURES", "spot": 15.80, "fcf": 2.00, "ev": 0.0, "pe": 0.0, "rsi": 35.0, "stoch": 28.0, "rel": 0.0, "short": 0.0, "val_a": 2.00},
")
    end = txt.find("    }", start) + 5
    txt = txt[:start] + presets_code + txt[end:]
    p.write_text(txt)
    print("[M82_PATCH] -> Presets de Wall Street, ETFs y Crypto inyectados con éxito.")
else:
    print("[M82_PATCH] -> No se localizó el diccionario PRESETS.")
PYEOF

chmod +x ~/M82/m82_dossier.py
~/M82/m82_git_shield.sh
