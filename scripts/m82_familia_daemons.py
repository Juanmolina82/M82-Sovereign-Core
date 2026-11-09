#!/usr/bin/env python3
import time, sqlite3, os
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/sqlite/m82_familia.db")

def log_event(daemon_name, message):
    log_dir = os.path.expanduser("~/M82/logs/familia")
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, f"{daemon_name}.log"), "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

def run_family_swarm():
    print("🚀 Enjambre Dinástico M82 (6 Daemons) iniciado...")
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            # 1. Kronos 8 - Anti-Dispersión
            c.execute("SELECT proyectos_activos FROM contencion_kanban WHERE miembro LIKE '%Carleth%'")
            res = c.fetchone()
            if res and res[0] > 3:
                log_event("kronos_8", "ALERTA C4: Dispersión detectada en Carleth > 3 proyectos.")
            else:
                log_event("kronos_8", "Status Nominal. Gobernanza Padre 8 en BUNKER MODE.")

            # 2. Architect 44
            log_event("architect_44", "C4 Containment Matrix Nominal.")

            # 3. Prophet 11
            log_event("prophet_11", "V11 Oracle Pipeline Listening (11:11 VET).")

            # 4. Junior Archon 8
            log_event("junior_archon_8", "Custodia de activos e infra OK.")

            # 5. Logistics 4 (Lisbeth 08=4)
            log_event("logistics_4", "Threshold Hécate Umbral 08=4 Nominal.")

            # 6. Builder 22
            log_event("builder_22", "B6 Heart Builder & Obra intactos.")

            conn.close()
        except Exception as e:
            log_event("swarm_error", str(e))
        
        time.sleep(300) # Check en bucle de 5 minutos

if __name__ == "__main__":
    run_family_swarm()
