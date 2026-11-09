import os, sqlite3, sys

# Inyectar tolerancia de tickers futuros en el CLI local
cli_path = os.path.expanduser("~/M82/m82")
if os.path.exists(cli_path):
    with open(cli_path, "r") as f:
        content = f.read()
    if "'CLc1'" not in content:
        content = content.replace(
            "TICKERS_DISPONIBLES =",
            "TICKERS_DISPONIBLES = ['CLc1', 'LCOc1', 'GCc1', 'ESc1', 'NQc1', 'VXc1', 'SIc1', 'HGc1'] +"
        )
        with open(cli_path, "w") as f:
            f.write(content)
        print("[M82 CLI] ✅ Habilitado soporte para consulta directa de Futuros en CLI.")
