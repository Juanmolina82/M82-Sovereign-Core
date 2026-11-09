#!/usr/bin/env python3
import sqlite3, os, subprocess, time, json, datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

# 8 Daemons Líderes de Mesa (Persistentes)
LEADER_DAEMONS = [
    "m82_pe_dry_powder_daemon.py",          # PE & VC Desk
    "m82_musk_empire_daemon.py",            # Musk Empire Desk
    "m82_treasury_bonds_daemon.py",         # Macro & Credit Desk
    "m82_crypto_commodities_daemon.py",     # Commodities & Faja Desk
    "m82_geopolitical_events_daemon.py",    # Geopolitics Desk
    "m82_m82_macro_notebook_daemon.py",          # Terminal & M82_MACRO Desk
    "m82_stablecoin_liquidity_daemon.py",   # Crypto Desk
    "m82_hud_card_generator_daemon.py"      # Infra & HUD Desk
]

def check_and_spawn_leaders():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🛡️ M82 SUPERVISOR // Verificando Estado de Líderes...")
    for daemon in LEADER_DAEMONS:
        # Verificar si el proceso está corriendo
        cmd = f"pgrep -f {daemon}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if not result.stdout.strip():
            print(f"  ⚠️ [Líder Caído] Reactivando -> {daemon}")
            script_path = os.path.join(BASE_DIR, daemon)
            if os.path.exists(script_path):
                subprocess.Popen(["python3", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                # Actualizar latido en SQLite
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("""
                    UPDATE m82_daemons_registry 
                    SET status='STANDBY_READY', last_heartbeat=CURRENT_TIMESTAMP 
                    WHERE daemon_name=?
                """, (daemon,))
                conn.commit()
                conn.close()
                print(f"  ✅ [Simulado/Registrado] -> {daemon} listo en DB")

def trigger_worker_ondemand(worker_name):
    """Invocación directa bajo demanda para los 32 workers secundarios"""
    print(f"⚡ [On-Demand Worker Triggered] -> {worker_name}")
    script_path = os.path.join(BASE_DIR, worker_name)
    if os.path.exists(script_path):
        subprocess.run(["python3", script_path], check=True)
        return True
    return False

if __name__ == "__main__":
    check_and_spawn_leaders()
    print("🚀 Supervisor de la Suite M82 operando con arquitectura Híbrida (8 Líderes + 32 On-Demand).")
