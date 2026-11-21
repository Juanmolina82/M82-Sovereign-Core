import sqlite3, os

# 1. Asegurar tabla daemons_registry para compatibilidad
conn = sqlite3.connect('m82_database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS daemons_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_id TEXT UNIQUE,
    state TEXT,
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Poblar estados de los daemons
daemons = [
    ('m82_ib_gateway', 'ACTIVE'),
    ('m82_macro_wire', 'ACTIVE'),
    ('m82_treasury_engine', 'ACTIVE'),
    ('m82_crypto_corridor', 'ACTIVE'),
    ('m82_telegram_bot', 'ACTIVE')
]

for d_id, st in daemons:
    cursor.execute("""
        INSERT INTO daemons_registry (daemon_id, state)
        VALUES (?, ?)
        ON CONFLICT(daemon_id) DO UPDATE SET state=?, last_heartbeat=CURRENT_TIMESTAMP
    """, (d_id, st, st))

conn.commit()
conn.close()

# 2. Purga de logs antiguos con nombres de marcas externas
log_files = ['m82/lite_runner.log', 'm82_ib.log', 'logs/api.log']
replacements = {"M82_WIRE": "M82_MACRO", "Reuters": "M82_WIRE", "M82_WIRE": "M82_WIRE"}

for lf in log_files:
    if os.path.exists(lf):
        with open(lf, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        with open(lf, 'w', encoding='utf-8') as f:
            for line in lines:
                for old, new in replacements.items():
                    line = line.replace(old, new)
                f.write(line)

print("✅ Tabla 'daemons_registry' sincronizada y logs purgados.")
