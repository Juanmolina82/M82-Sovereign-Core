#!/usr/bin/env python3
import sqlite3, os, time, subprocess
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def ingest_venalum_dossier():
    if not os.path.exists(DB_PATH):
        print(f"❌ No se encontró la base de datos en {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    cursor = conn.cursor()

    now_date = datetime.now().strftime("%Y-%m-%d")

    # 1. Asentar Ticker de Operación y Offtake Venalum (Mercuria / Glencore / Heeney)
    headline_venalum = (
        "Mercuria Glencore Heeney bidding for Venalum operation 15k ton G20 shipment - "
        "Integrated bauxite Los Pijiguaos (300Mt) + Interalumina + Guri Hydro power play"
    )
    cursor.execute("""
        INSERT INTO m82_manual_notes (date, ticker, valor, fuente, enviado_bot)
        VALUES (?, 'VENALUM_OFFTAKE_MERCURIA', ?, 'Bloomberg_EnergyDesk', 1)
    """, (now_date, headline_venalum))

    # 2. Asentar Score de Riesgo del Dossier #139
    cursor.execute("""
        INSERT INTO m82_manual_notes (date, ticker, valor, fuente, enviado_bot)
        VALUES (?, 'DOSSIER_139_RISK_SCORE', '8.2', 'Bloomberg_Refinitiv', 1)
    """, (now_date,))

    conn.commit()

    # 3. Consultar y verificar la inserción en la consola
    cursor.execute("""
        SELECT id, date, ticker, valor, enviado_bot 
        FROM m82_manual_notes 
        ORDER BY id DESC LIMIT 5
    """)
    rows = cursor.fetchall()
    conn.close()

    print("\n✅ DOSSIER #139 INDEXADO CON ÉXITO EN SQLITE (WAL):")
    print("=" * 70)
    for row in rows:
        print(f"ID {row[0]} | {row[1]} | {row[2]:<25} | {str(row[3])[:30]}... | enviado_bot={row[4]}")
    print("=" * 70)

    # 4. Sincronizar tarjeta hacia la Galería de Android
    sync_script = os.path.expanduser("~/M82/m82_sync_gallery.py")
    if os.path.exists(sync_script):
        subprocess.run(["python3", sync_script], check=False)

if __name__ == "__main__":
    ingest_venalum_dossier()
