#!/usr/bin/env python3
import sqlite3, os

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Eliminar duplicados existentes manteniendo solo el primer registro
cursor.execute("""
    DELETE FROM m82_multi_stream
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM m82_multi_stream
        GROUP BY headline
    );
""")

# 2. Re-asegurar que la columna headline tenga índice UNIQUE
try:
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_headline_unique ON m82_multi_stream(headline);")
    print("✅ Índice UNIQUE aplicado correctamente a 'headline'.")
except Exception as e:
    print(f"⚠️ Nota sobre índice: {e}")

conn.commit()
conn.close()

print("🧹 Limpieza de duplicados completada en m82_database.db.")
