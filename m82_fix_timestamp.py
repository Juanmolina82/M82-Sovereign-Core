#!/usr/bin/env python3
import os
import sqlite3
import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB_PATH, timeout=30.0)
c = conn.cursor()

now = datetime.datetime.now().isoformat()

# 1. Asegurar la columna 'timestamp' en m82_mcn_checklist
try:
    c.execute("ALTER TABLE m82_mcn_checklist ADD COLUMN timestamp TEXT;")
except sqlite3.OperationalError:
    pass # La columna ya existe

# 2. Inserción adaptada a las columnas de m82_mcn_checklist
brent, squeeze, real_yield = 106.14, 13.14, 3.0
c.execute("""
INSERT INTO m82_mcn_checklist 
(timestamp, brent_price, dubai_squeeze, red_day_flag, consecutive_red_days, diesel_shortage_active, real_yield) 
VALUES (?, ?, ?, 1, 1, 1, ?);
""", (now, brent, squeeze, real_yield))

# 3. Insertar la señal final en la cola multi-stream
headline_electoral = f"M82 VS FINAL: Brent {brent} + {squeeze} = {brent+squeeze:.2f} Físico | Reservas 20% Chávez vs 5-8% real M82_MACRO fake | Narrativa electoral."
c.execute("""
INSERT INTO m82_multi_stream 
(daemon_source, headline, status, timestamp) 
VALUES ('M82_AUDIOS_ELECTORAL_FINAL', ?, 'PENDING', ?);
""", (headline_electoral, now))

conn.commit()
conn.close()

print("✅ MIGRACIÓN COMPLETADA: Columna 'timestamp' integrada e inyección realizada correctamente.")
