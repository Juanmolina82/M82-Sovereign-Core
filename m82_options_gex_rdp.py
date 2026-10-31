import os, sys, sqlite3
from datetime import datetime

try:
    import refinitiv.data as rd
except ImportError:
    pass

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
APP_KEY = os.getenv("REFINITIV_APP_KEY", "TU_APP_KEY_AQUI")
TARGET_MEGACAPS = ['NVDA.O', 'MSFT.O', 'AAPL.O', 'META.O', 'AMZN.O', 'GOOGL.O', 'TSLA.O', 'SPY']

def calculate_rdp_gex():
    try:
        rd.open_session(app_key=APP_KEY)
        print("🎯 [RDP REAL-TIME GEX] Extrayendo cadenas de opciones oficiales...")
        
        # Consulta de volúmenes Put/Call y Open Interest en cadena
        gex_data = rd.get_data(
            universe=TARGET_MEGACAPS,
            fields=['TR.CallVolumeTotal', 'TR.PutVolumeTotal', 'TR.ImpliedVola1M']
        )
        
        for _, row in gex_data.iterrows():
            ric = row.get('Instrument', '')
            call_vol = row.get('CallVolumeTotal', 1) or 1
            put_vol = row.get('PutVolumeTotal', 0) or 0
            pc_ratio = put_vol / call_vol if call_vol > 0 else 1.0
            
            print(f"  └─ {ric}: Put/Call Ratio: {pc_ratio:.2f}")

    except Exception as e:
        print(f"❌ Error al consultar GEX en RDP: {e}")
    finally:
        try:
            rd.close_session()
        except:
            pass

if __name__ == "__main__":
    calculate_rdp_gex()
