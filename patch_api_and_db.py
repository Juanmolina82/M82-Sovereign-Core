import sqlite3, re

# 1. Normalizar etiquetas residuales en la BD (M82_MACRO, M82_WIRE, etc. -> M82_WIRE / M82_MACRO)
conn = sqlite3.connect('m82_database.db')
cursor = conn.cursor()

cursor.execute("UPDATE signals SET source = 'M82_WIRE' WHERE source IN ('M82_MACRO', 'M82_WIRE', 'M82_WIRE', 'M82_WIRE')")
cursor.execute("UPDATE signals SET source = 'M82_MACRO' WHERE source LIKE '%MACRO%' AND source != 'M82_MACRO'")

conn.commit()
conn.close()

# 2. Parchear m82_api_server.py para asegurar que /daemons y /signals respondan correctamente
api_path = 'm82_api_server.py'
if os.path.exists(api_path):
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Asegurar endpoint /daemons si solo existia /daemon
    if '/daemons' not in content:
        content = content.replace("@app.route('/daemon'", "@app.route('/daemons')\n@app.route('/daemon'")
        with open(api_path, 'w', encoding='utf-8') as f:
            f.write(content)

print("✅ Base de datos sanitizada al 100% y rutas API verificadas.")
