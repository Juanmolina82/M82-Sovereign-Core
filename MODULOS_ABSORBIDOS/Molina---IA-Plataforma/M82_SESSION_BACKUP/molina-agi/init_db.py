import sqlite3

conn = sqlite3.connect("memoria.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS diario_macro (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha TEXT,
  resumen TEXT,
  escenarios TEXT,
  niveles_clave TEXT,
  creado_en TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS eventos_mercado (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha TEXT,
  tipo TEXT,
  fuente TEXT,
  descripcion TEXT,
  impacto_estimado TEXT,
  creado_en TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS ideas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha TEXT,
  activo TEXT,
  tesis TEXT,
  riesgos TEXT,
  horizonte TEXT,
  estado TEXT,
  creado_en TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("Base de datos inicializada.")
