#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

conn = sqlite3.connect(DB_PATH, timeout=60.0)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")
c = conn.cursor()

# 1. Agregar columna real_yield si no existe en la tabla previa
try:
    c.execute("ALTER TABLE m82_mcn_checklist ADD COLUMN real_yield REAL;")
    print("✅ Columna 'real_yield' agregada exitosamente.")
except sqlite3.OperationalError:
    print("ℹ️ La columna 'real_yield' ya existe.")

# 2. Insertar snapshot actualizado
now = datetime.datetime.now().isoformat()
c.execute("""
    INSERT INTO m82_mcn_checklist (timestamp, brent_price, dubai_squeeze, red_day_flag, consecutive_red_days, diesel_shortage_active, real_yield)
    VALUES (?, 107.2, 13.14, 1, 1, 1, 3.30)
""", (now,))

conn.commit()
conn.close()
print("🚀 ESQUEMA DE BASE DE DATOS SINCRONIZADO Y OPERATIVO.")
