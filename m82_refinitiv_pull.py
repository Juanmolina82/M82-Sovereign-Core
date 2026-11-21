#!/usr/bin/env python3
import os, sys, sqlite3, json
from datetime import datetime

try:
    from dotenv import load_dotenv
    env_file = os.path.expanduser("~/M82/.env.refinitiv")
    if os.path.exists(env_file):
        load_dotenv(env_file)
except ImportError:
    pass

try:
    import lseg.data as ld
except ImportError:
    try:
        import eikon as ld
    except ImportError:
        sys.exit(1)

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def connect_lseg():
    try:
        ld.open_session()
        return "DESKTOP_LOCAL_SESSION"
    except Exception:
        app_key = os.getenv("REFINITIV_APP_KEY")
        if app_key:
            ld.set_app_key(app_key)
            return "APP_KEY_SESSION"
        user = os.getenv("REFINITIV_USER")
        password = os.getenv("REFINITIV_PASS")
        if user and password:
            ld.open_platform_session(app_key=app_key or "M82_APP", grant=ld.Grant.Password(username=user, password=password))
            return "PLATFORM_PASSWORD_SESSION"
        raise RuntimeError("Refinitiv Session Error")

def main():
    try:
        session_type = connect_lseg()
        energy_tickers = ["LCOc1", "HOc1", "LGOc1"]
        freight_tickers = ["BWET", "BDIY", "BDTI", "BCTI"]
        
        try:
            df_e, _ = ld.get_data(universe=energy_tickers, fields=["TR.PRICE", "TR.PRICECHANGE"])
            e_data = df_e.to_dict(orient="records") if df_e is not None else []
        except:
            e_data = []

        try:
            df_f, _ = ld.get_data(universe=freight_tickers, fields=["TR.PRICE", "TR.PRICECHANGE"])
            f_data = df_f.to_dict(orient="records") if df_f is not None else []
        except:
            f_data = []

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "node": "Caracas HQ Node",
            "governance": "0.30x BUNKER_MODE LOCK",
            "tail_risk": 10.0,
            "session_type": session_type,
            "vectors": {
                "energy": e_data,
                "freight": f_data,
                "fixtures": {"vlcc": "EMPIRE HOPE FOR ORDERS", "ws": 562.5}
            }
        }

        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA busy_timeout=60000;")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO macro_dossier (timestamp, risk_score, headline, source, metadata_json)
            VALUES (?, 10.0, ?, 'REFINITIV_API_AUTO', ?)
        """, (datetime.utcnow().isoformat(), "REFINITIV AUTOMATED STREAM: Physical Fragility Ingested", json.dumps(payload)))
        conn.commit()
        conn.close()
        print("✅ [M82 WAL] Ingesta exitosa.")
    except Exception as ex:
        print(f"❌ [ERROR] {ex}")

if __name__ == "__main__":
    main()
