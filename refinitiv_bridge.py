#!/usr/bin/env python3
import os
import sys
import json
import sqlite3
import logging
from datetime import datetime

LOG_FILE = os.path.expanduser("~/M82/refinitiv_bridge.log")
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
VAULT_PATH = os.path.expanduser("~/M82/vault.json")

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_lseg_credentials():
    if os.path.exists(VAULT_PATH):
        try:
            with open(VAULT_PATH, "r") as f:
                vault = json.load(f)
                app_key = (
                    vault.get("LSEG_APP_KEY_CORE") or 
                    vault.get("LSEG_APP_KEY") or 
                    vault.get("LSEG_APP_KEY_SOVEREIGN")
                )
                user = vault.get("LSEG_USER")
                return app_key, user
        except Exception as e:
            logging.error(f"Error leyendo vault.json: {e}")
    return os.getenv("LSEG_APP_KEY"), os.getenv("LSEG_USER")

def pull_lseg_data(rics):
    app_key, user = load_lseg_credentials()
    if not app_key:
        logging.error("LSEG_APP_KEY no encontrada en vault.json")
        return None

    try:
        import refinitiv.data as rd
        rd.open_session(app_key=app_key)
        df = rd.get_data(rics, fields=["DSPLY_NAME", "CF_LAST", "NETCHNG_1", "PCTCHNG"])
        rd.close_session()
        return df
    except ImportError:
        logging.warning("Libreria 'refinitiv.data' no detectada en entorno local. Operando via HTTP / Mock Stream...")
        return None
    except Exception as e:
        logging.error(f"Error durante pull LSEG: {e}")
        return None

if __name__ == "__main__":
    app_key, user = load_lseg_credentials()
    if not app_key:
        print("⚠️ ALERTA: No se detecto ninguna App Key valida en ~/M82/vault.json")
    else:
        print(f"🟢 LSEG Credentials cargadas exitosamente para: {user}")
        print(f"🔑 App Key activa: {app_key[:8]}...{app_key[-6:]}")
        print("Iniciando puente de ingesta Refinitiv Workspace / LSEG...")
