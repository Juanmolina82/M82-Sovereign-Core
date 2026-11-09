#!/usr/bin/env python3
import sqlite3, json, sys, os, subprocess

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def dump_all_and_dispatch(news_list):
    """
    Recibe una lista de tuplas con formato:
    [(headline, source, category, risk_score, m82_tag, sentiment, entities), ...]
    Guarda TODO en la BD y dispara el bot de alertas.
    """
    if not os.path.exists(DB_PATH):
        print("❌ [BD] La base de datos no existe.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    count = 0
    for item in news_list:
        headline, source, category, risk_score, m82_tag, sentiment, entities = item
        meta_json = json.dumps({"source_ref": source, "ingest_mode": "FULL_DUMP"})
        
        c.execute('''
            INSERT INTO macro_dosier (headline, source, category, risk_score, m82_tag, metadata_json, sentiment, entities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (headline, source, category, float(risk_score), m82_tag, meta_json, sentiment, entities))
        count += 1

    conn.commit()
    conn.close()
    print(f"🔥 [M82 DUMP] ¡Procesados e ingestados {count} eventos exitosamente!")

    # Ejecutar el despachador de tarjetas y alertas
    bot_script = os.path.expanduser("~/M82/m82_telegram_bot.py")
    if os.path.exists(bot_script):
        subprocess.run(["python3", bot_script])

if __name__ == "__main__":
    print("Módulo de Ingesta Masiva M82 activo.")
