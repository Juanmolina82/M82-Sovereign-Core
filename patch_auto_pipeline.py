import re

api_path = "m82_api_server.py"

with open(api_path, "r") as f:
    code = f.read()

# Insertar middleware de auto-ejecución antes del return principal de la API
auto_exec_code = '''
        # AUTO-EXECUTION ENGINE (Zero-Touch M82)
        import sqlite3
        try:
            conn = sqlite3.connect('m82_database.db')
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS m82_geopolitical_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT, risk_score REAL, headline TEXT, actors TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Auto-inyectar hallazgos detectados en el digest
            if "GM" in prompt_text or "General Motors" in prompt_text:
                c.execute("INSERT INTO m82_geopolitical_events (source, risk_score, headline, actors) VALUES (?, ?, ?, ?)",
                          ('GM_HEDGE_US', 0.15, 'GM Buy Target $105 - US Proxy Consumo vs Faja Hedge', 'GM, WALL_STREET, ZACKS'))
            if "DIESEL" in prompt_text or "DIÉSEL" in prompt_text:
                c.execute("INSERT INTO m82_geopolitical_events (source, risk_score, headline, actors) VALUES (?, ?, ?, ?)",
                          ('DIESEL_BAN_US', 0.92, 'US Diesel Export Ban - Impacto Critico en Dilucion Merey 16 Faja', 'M82_MACRO_ENERGIA, TRUMP, PDVSA'))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Auto-injection bypass log:", e)
'''

if "AUTO-EXECUTION ENGINE" not in code:
    # Insertar el bloque de auto-ejecución
    patched_code = code.replace("def query_agent():", "def query_agent():\n" + auto_exec_code)
    with open(api_path, "w") as f:
        f.write(patched_code)
    print("✅ Parche de auto-ejecución aplicado correctamente a m82_api_server.py")
else:
    print("⚡ El motor de auto-ejecución ya está activo.")
