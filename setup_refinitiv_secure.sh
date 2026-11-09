#!/usr/bin/env bash
cd ~/M82 || exit 1

echo "========================================================================="
echo "   M82 SOVEREIGN CORE v63.0.01-A :: SECURE REFINITIV LIVE BRIDGE SETUP  "
echo "========================================================================="

# 1. Protección estricta en .gitignore
cat << 'EOF_GIT' > ~/M82/.gitignore
*.db
*.db-wal
*.db-shm
*.db_backup*
__pycache__/
*.pyc
.env
*.log
*credential*
*secret*
EOF_GIT

# 2. Plantilla local .env
if [ ! -f ~/M82/.env ]; then
cat << 'EOF_ENV' > ~/M82/.env
# REFINITIV RDP CREDENTIALS - LOCAL NODE ONLY (DO NOT COMMIT)
RDP_APP_KEY=
RDP_USER=
RDP_PASS=
EOF_ENV
chmod 600 ~/M82/.env
echo "[SECURITY] Archivo ~/M82/.env creado con permisos 600."
fi

# 3. Instalación de paquetes Python requeridos
pip install refinitiv-data pandas python-dotenv --quiet

# 4. Creación del Puente Seguro Refinitiv -> SQLite (m82_live_prices)
cat << 'EOF_BRIDGE' > ~/M82/m82_refinitiv_bridge.py
#!/usr/bin/env python3
"""
M82 Sovereign Core v63.0.01-A - Refinitiv Workspace / RDP Live Data Bridge
Node: Charallave L4/L5 Edge
"""

import os
import sys
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/M82/.env"))

try:
    import refinitiv.data as rd
    HAS_RD = True
except ImportError:
    HAS_RD = False
    print("[M82_ERROR] 'refinitiv-data' no instalado. Ejecute: pip install refinitiv-data")

def init_session():
    if not HAS_RD:
        return False
    app_key = os.getenv("RDP_APP_KEY", "").strip()
    user = os.getenv("RDP_USER", "").strip()
    pwd = os.getenv("RDP_PASS", "").strip()
    
    if not app_key or not user or not pwd:
        print("\n[M82 WARNING] Credenciales incompletas en ~/M82/.env")
        print("[M82 INSTRUCTION] Complete RDP_APP_KEY, RDP_USER y RDP_PASS con 'nano ~/M82/.env'\n")
        return False
        
    try:
        # Intento 1: Desktop Session (Workspace abierto en red)
        try:
            rd.open_session(name="desktop.workspace")
            print("[M82_REFINITIV] Conectado a Refinitiv Workspace Desktop Session.")
            return True
        except Exception:
            pass
            
        # Intento 2: Platform Cloud Session
        sess = rd.session.platform.Definition(
            app_key=app_key,
            grant=rd.session.platform.Grant.Password(username=user, password=pwd)
        ).get_session()
        sess.open()
        rd.set_default_session(sess)
        print("[M82_REFINITIV] Conectado exitosamente a Refinitiv Data Platform (Cloud).")
        return True
    except Exception as e:
        print(f"[M82_ERROR] Fallo de autenticación en Refinitiv: {e}")
        return False

def fetch_live_data(tickers):
    fields = ["CF_LAST", "TR.FCFYield", "TR.EVToEBITDA", "TR.PE"]
    try:
        df = rd.get_data(universe=tickers, fields=fields)
        return df
    except Exception as e:
        print(f"[M82_ERROR] Fallo al extraer telemetría: {e}")
        return None

def save_to_live_table(df):
    if df is None or df.empty:
        return
        
    db_path = os.path.expanduser("~/M82/m82_database.db")
    conn = sqlite3.connect(db_path, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS m82_live_prices (
        ticker TEXT PRIMARY KEY,
        spot REAL NOT NULL,
        fcf REAL,
        ev_ebitda REAL,
        forward_pe REAL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    for _, row in df.iterrows():
        raw_ticker = str(row.get("Instrument", "")).strip()
        # Mapeo universal de Tickers
        ticker = raw_ticker.replace(".N", "").replace(".O", "").replace("=", "")
        if raw_ticker == "DELL.N": ticker = "DELL.N"  # Preserva tag exacto
        
        spot = float(row.get("CF_LAST") or 0.0)
        fcf = float(row.get("TR.FCFYield") or 0.0)
        ev = float(row.get("TR.EVToEBITDA") or 0.0)
        pe = float(row.get("TR.PE") or 0.0)
        
        if spot > 0:
            cursor.execute("""
            INSERT OR REPLACE INTO m82_live_prices (ticker, spot, fcf, ev_ebitda, forward_pe, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
            """, (ticker, spot, fcf, ev, pe))
            print(f"[LIVE REFINITIV INGEST] {ticker} -> Spot: ${spot:.2f} | FCF: {fcf:.2f}% | P/E: {pe:.2f}x")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if init_session():
        universe = ["DELL.N", "NVDA.O", "AAPL.O", "MSFT.O", "XAU=", "LCOc1", "HGc1"]
        data = fetch_live_data(universe)
        if data is not None:
            print("\n" + "=" * 74)
            print("         REFINITIV WORKSPACE :: TELEMETRÍA DE MERCADO EN VIVO           ")
            print("=" * 74)
            print(data.to_string())
            print("=" * 74 + "\n")
            save_to_live_table(data)
            print("[M82 SYSTEM] Ingesta viva completada en la tabla 'm82_live_prices'.\n")
EOF_BRIDGE

chmod +x ~/M82/m82_refinitiv_bridge.py

# 5. Parche en m82_dossier.py para priorizar la tabla m82_live_prices sobre PRESETS
python3 - << 'PY_LIVE_PATCH'
import pathlib

p = pathlib.Path.home() / "M82" / "m82_dossier.py"
t = p.read_text()

live_override_code = """
def get_asset_data(ticker):
    # 1. Consulta prioritaria en tabla en vivo m82_live_prices
    try:
        import sqlite3
        db_path = os.path.expanduser("~/M82/m82_database.db")
        conn = sqlite3.connect(db_path, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute("SELECT spot, fcf, ev_ebitda, forward_pe FROM m82_live_prices WHERE ticker = ? OR ticker = ? LIMIT 1", (ticker, ticker + ".N"))
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0] and float(row[0]) > 0:
            base = PRESETS.get(ticker, {"name": ticker, "rsi": 50.0, "stoch": 50.0, "rel_pe": 1.0, "short": 1.0, "verdict": "DATOS EN VIVO REFINITIV"})
            d = dict(base)
            d["spot"] = float(row[0])
            if row[1] and float(row[1]) > 0: 
                d["fcf"] = float(row[1])
                d["val_a"] = float(row[1])
            if row[2]: d["ev"] = float(row[2])
            if row[3]: d["pe"] = float(row[3])
            d["name"] = d.get("name", ticker) + " [LIVE REFINITIV]"
            print(f"[M82 TELEMETRY] -> PRECIO EN VIVO REFINITIV UTILIZADO: ${d['spot']:.2f} (Preset Ignorado)")
            return d
    except Exception as e:
        pass
        
    return PRESETS.get(ticker)
"""

if "def get_asset_data" not in t:
    # Inyecta la función de resolución de datos viva
    t = live_override_code + "\n" + t
    t = t.replace('data = PRESETS[ticker]', 'data = get_asset_data(ticker)')
    p.write_text(t)
    print("[PATCH OK] 'm82_dossier.py' actualizado: Prioridad a datos telemétricos en vivo.")
else:
    print("[PATCH INFO] La lógica de priorización telemétrica ya está activa.")
PY_LIVE_PATCH

chmod +x ~/M82/m82_dossier.py
echo -e "\n[CONFIGURACIÓN SECRETA COMPLETADA] -> Edite ~/M82/.env para ingresar sus credenciales RDP."
