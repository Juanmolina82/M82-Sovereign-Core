#!/usr/bin/env python3
import os
import sqlite3
import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB_PATH, timeout=30.0)
c = conn.cursor()

now = datetime.datetime.now().isoformat()

# 1. Creación de Esquema Integrado
c.executescript("""
CREATE TABLE IF NOT EXISTS m82_mcn_checklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    brent_price REAL,
    dubai_squeeze REAL,
    red_day_flag INTEGER,
    consecutive_red_days INTEGER,
    diesel_shortage_active INTEGER,
    real_yield REAL
);

CREATE TABLE IF NOT EXISTS m82_multi_stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_source TEXT,
    headline TEXT,
    status TEXT DEFAULT 'PENDING',
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS m82_narrativa_electoral (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    claim TEXT,
    realidad TEXT,
    precedente TEXT,
    impacto_m82 TEXT
);
""")

# 2. Inyección de MCN Checklist Actualizado
brent, squeeze, real_yield = 106.14, 13.14, 3.0
c.execute("""INSERT INTO m82_mcn_checklist 
(timestamp, brent_price, dubai_squeeze, red_day_flag, consecutive_red_days, diesel_shortage_active, real_yield) 
VALUES (?, ?, ?, 1, 1, 1, ?);""", (now, brent, squeeze, real_yield))

# 3. Inyección de Narrativa Electoral y Reservas
claim = "Empresa privada con reservas más altas del mundo entre privados - colosal - 300MM OPESPI - 1 trillion in situ."
realidad = "Estimado no extraíble en 25 años - 5-8% real vs 20% Chávez - recurso != reserva M82_MACRO - SAGD canadiense nunca hecho VE."
precedente = "Acuerdos minerales Ucrania US - anuncio rimbombante sin ejecución."
impacto = "VS 35% equity penny warrants + 20% at cost $300M 170k/350k bpd no mueve Brent 106.14+13.14=119.28 físico | Triangulación JPB - riesgo político sube."

c.execute("""INSERT INTO m82_narrativa_electoral 
(timestamp, claim, realidad, precedente, impacto_m82) 
VALUES (?, ?, ?, ?, ?);""", (now, claim, realidad, precedente, impacto))

# 4. Inyección en Multi-Stream
headline_electoral = f"M82 VS FINAL: Brent {brent} + {squeeze} = {brent+squeeze:.2f} Físico | Reservas 20% Chávez vs 5-8% real M82_MACRO fake | Narrativa electoral."
c.execute("""INSERT INTO m82_multi_stream 
(daemon_source, headline, status, timestamp) 
VALUES ('M82_AUDIOS_ELECTORAL_FINAL', ?, 'PENDING', ?);""", (headline_electoral, now))

conn.commit()
conn.close()

print("✅ Infraestructura unificada exitosamente. Cero errores de sintaxis/atributos.")
