#!/usr/bin/env bash
cd ~/M82 || exit 1

echo "========================================================================="
echo "   M82 SOVEREIGN CORE v63.0.01-A :: LSEG REFINITIV ENV STANDARDIZER     "
echo "========================================================================="

# 1. Asegurar resguardo de secretos en .gitignore
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

# 2. Actualizar ~/M82/.env manteniendo Telegram y adaptando LSEG/RDP
cat << 'EOF_ENV' > ~/M82/.env
# M82 SOVEREIGN NODE SECRETS - CUSTODIA PASIVA 0.30x LOCK
LSEG_APP_KEY=374da013581c4eebd927692224
LSEG_USER=juanmolina82@gmail.com
LSEG_PASS=SU_PASSWORD_REFINITIV_AQUI

# Aliases de compatibilidad directa para RDP/Eikon Bridge
RDP_APP_KEY=374da013581c4eebd927692224
RDP_USER=juanmolina82@gmail.com
RDP_PASS=SU_PASSWORD_REFINITIV_AQUI

# Integraciones Auxiliares
AISHUB_KEY=INSERTAR_TU_AISHUB_KEY_AQUI
TELEGRAM_BOT_TOKEN=8600412468:AAHiBNgu230J01IzeqL7rZOR
TELEGRAM_CHAT_ID=-1004335849125
EOF_ENV

chmod 600 ~/M82/.env

# 3. Reescribir el puente para soportar automáticamente LSEG_APP_KEY y RDP_APP_KEY
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
        
    app_key = (os.getenv("RDP_APP_KEY") or os.getenv("LSEG_APP_KEY") or "").strip()
    user = (os.getenv("RDP_USER") or os.getenv("LSEG_USER") or "").strip()
    pwd = (os.getenv("RDP_PASS") or os.getenv("LSEG_PASS") or "").strip()
    
    if not app_key or not user or "SU_PASSWORD" in pwd:
        print("\n[M82 WARNING] Credenciales de LSEG/Refinitiv incompletas en ~/M82/.env")
        print("[M82 INSTRUCTION] Abra Termux y ejecute: nano ~/M82/.env")
        print("[M82 INSTRUCTION] Reemplace 'SU_PASSWORD_REFINITIV_AQUI' por su contraseña real de Refinitiv.\n")
        return False
        
    try:
        # Intento 1: Desktop Session (Si Workspace está corriendo en la red local)
        try:
            rd.open_session(name="desktop.workspace")
            print("[M82_REFINITIV] Conectado a Refinitiv Workspace Desktop Session.")
            return True
        except Exception:
            pass
            
        # Intento 2: Platform Cloud Session directa
        sess = rd.session.platform.Definition(
            app_key=app_key,
            grant=rd.session.platform.Grant.Password(username=user, password=pwd)
        ).get_session()
        sess.open()
        rd.set_default_session(sess)
        print("[M82_REFINITIV] Conectado exitosamente a Refinitiv Data Platform (Cloud Session).")
        return True
    except Exception as e:
        print(f"[M82_ERROR] Fallo de autenticación en Refinitiv RDP: {e}")
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
        ticker = raw_ticker.replace(".N", "").replace(".O", "").replace("=", "")
        if raw_ticker == "DELL.N": ticker = "DELL.N"
        
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
echo "[M82 FIX] Parche instalado. Complete su contraseña en ~/M82/.env"
