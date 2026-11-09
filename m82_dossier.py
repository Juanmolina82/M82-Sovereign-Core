#!/usr/bin/env python3
import sys

PRESETS = {
    "DELL.N": {"name": "Dell Technologies Inc.", "sector": "TECHNOLOGY", "spot": 118.50, "fcf": 4.75, "rsi": 42.1, "val_a": 4.75},
    "NVDA":   {"name": "NVIDIA Corporation", "sector": "SEMICONDUCTORS", "spot": 125.40, "fcf": 2.10, "rsi": 61.2, "val_a": 2.10},
    "CLc1":   {"name": "WTI Crude Oil Future", "sector": "ENERGY / FUTURES", "spot": 74.20, "fcf": 4.50, "rsi": 48.0, "val_a": 4.50},
    "LCOc1":  {"name": "Brent Crude Future", "sector": "ENERGY / FUTURES", "spot": 78.45, "fcf": 4.50, "rsi": 48.0, "val_a": 4.50},
    "GCc1":   {"name": "Gold Future", "sector": "METALS / FUTURES", "spot": 2738.50, "fcf": 7.79, "rsi": 55.0, "val_a": 7.79},
    "ESc1":   {"name": "S&P 500 Future", "sector": "INDEX / FUTURES", "spot": 5780.25, "fcf": 3.50, "rsi": 50.0, "val_a": 3.50},
    "VXc1":   {"name": "VIX Future", "sector": "VOLATILITY / FUTURES", "spot": 15.80, "fcf": 2.00, "rsi": 35.0, "val_a": 2.00}
}

if __name__ == '__main__':
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'CLc1'
    d = PRESETS.get(ticker)
    if d:
        line = '┌' + '─'*58 + '┐'
        head = '│ M82 DOSSIER TELEMETRY :: ' + f'{ticker:<31}' + '│'
        sep  = '├' + '─'*58 + '┤'
        n_str = '│ Asset Name : ' + f'{d.get("name", "N/A"):<43}' + '│'
        s_str = '│ Sector     : ' + f'{d.get("sector", "N/A"):<43}' + '│'
        p_str = '│ Spot Price : $' + f'{d.get("spot", 0.0):<42.2f}' + '│'
        f_str = '│ FCF Yield  : ' + f'{d.get("fcf", 0.0):<41.2f}' + '% │'
        r_str = '│ RSI (14D)  : ' + f'{d.get("rsi", 0.0):<43.1f}' + '│'
        v_str = '│ Val Alpha  : ' + f'{d.get("val_a", 0.0):<43.2f}' + '│'
        bot  = '└' + '─'*58 + '┘'
        print('\n' + '\n'.join([line, head, sep, n_str, s_str, p_str, f_str, r_str, v_str, bot]) + '\n')
    else:
        print('[M82] Ticker no encontrado: ' + str(ticker))
    sys.exit(0)
