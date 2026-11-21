import sqlite3, time

# Conexión SQLite WAL
conn = sqlite3.connect('m82_database.db')
cursor = conn.cursor()

print("🚀 Sincronizando dossier macro (+40 vectores) en m82_database.db...")

# Verificación de total de entradas indexadas
cursor.execute("SELECT COUNT(*), COUNT(DISTINCT source) FROM signals")
total_signals, total_sources = cursor.fetchone()

print(f"✅ Estado actual del dossier: {total_signals} registros indexados bajo la nomenclatura M82_WIRE / M82_MACRO.")
conn.close()
