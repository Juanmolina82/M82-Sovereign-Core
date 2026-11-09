import sqlite3
import pandas as pd

# 1. Leer el archivo CSV generado
df = pd.read_csv("bancos_refinitiv.csv")

# 2. Establecer conexión SQLite
conn = sqlite3.connect("m82_data.db")

# Activar el modo WAL directamente en la conexión
conn.execute("PRAGMA journal_mode=WAL;")

# 3. Migrar el DataFrame a la tabla SQLite
df.to_sql("cobertura_bancaria", conn, if_exists="replace", index=False)

# 4. Confirmar y cerrar conexión
conn.commit()
conn.close()

print("[SQLITE OK] Tabla 'cobertura_bancaria' migrada y persistida exitosamente en 'm82_data.db'.")
