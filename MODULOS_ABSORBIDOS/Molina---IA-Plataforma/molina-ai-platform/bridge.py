import json
import time
import os

def log_node_score(node_data):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] NODE: {node_data['name']} | SCORE: {node_data['fase3_score']} | CAT: {node_data['fase3_status']}\n"
    with open('fase3_history.log', 'a') as f:
        f.write(log_line)

def update_loop():
    messages = [
        "8 TANQUERS DETECTED - HORMUZ STRESS LEVEL HIGH",
        "CHEVRON PHASE 3: NODO ANCLA VALIDATED - SCORE: 91.5",
        "ENERGY FLOW: PLC 82K | PALITO 80K BPD",
        "GLOBAL RISK INDEX: 0.9705 - RED ALERT ACTIVE"
    ]
    idx = 0
    # Nodo de Chevron como base de auditoría
    chevron_data = {
        "name": "Chevron Petropiar",
        "fase3_score": 91.5,
        "fase3_status": "NODO ANCLA"
    }
    
    # Registrar el score inicial al arrancar
    log_node_score(chevron_data)

    while True:
        data = {
            "risk_index": 0.9705,
            "stargate_score": 85.4,
            "refinery_plc": 82000,
            "refinery_palito": 80000,
            "hormuz_alert": messages[idx % len(messages)],
            "fase3_status": chevron_data["fase3_status"],
            "fase3_score": chevron_data["fase3_score"]
        }
        with open('live_data.json', 'w') as f:
            json.dump(data, f)
        
        # Cada 10 ciclos (aprox 2.5 min), re-confirmamos el log
        if idx % 10 == 0:
            log_node_score(chevron_data)
            
        idx += 1
        time.sleep(15)

if __name__ == "__main__":
    update_loop()
