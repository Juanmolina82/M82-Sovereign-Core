#!/bin/bash
# ==============================================================================
# M82 V63.0.01-A :: DEPLOYMENT & MAINTENANCE SCRIPT MAESTRO
# Sede: Caracas HQ Central ⊗ Charallave Edge
# ==============================================================================

set -e

echo "=== [1/5] Preparando Entorno y Directorios ==="
mkdir -p ~/M82/app
cd ~/M82

echo "=== [2/5] Generando Frontend Sanitizado (PWA) ==="
cat > ~/M82/app/index.html << 'HTML'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>M82 Data Core V63.0.01-A</title>
    <style>
        body { background: #0a0a0a; color: #e5e5e5; font-family: monospace; padding: 16px; margin: 0; }
        .card { border: 1px solid #333; padding: 12px; margin-bottom: 8px; border-radius: 4px; }
        .head-title { font-size: 22px; color: #ffffff; font-weight: bold; }
        .sub-title { color: #00ff66; font-size: 14px; margin-bottom: 12px; }
        .ticker-group { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 12px; }
        .ticker { background: #141414; border: 1px solid #262626; padding: 8px 12px; border-radius: 4px; }
        .val { color: #00e5ff; font-weight: bold; }
        .alert-box { border-left: 3px solid #ff9900; background: #1a1500; padding: 8px 12px; margin-top: 8px; }
        .risk-box { border-left: 3px solid #00e5ff; background: #001a1a; padding: 8px 12px; margin-top: 8px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="head-title">M82 Data Core V63.0.01-A</div>
        <div class="sub-title">Caracas HQ Central ⊗ Charallave Edge</div>
        <div id="timestamp" style="color: #888; font-size: 12px; margin-bottom: 12px;">Cargando telemetría...</div>
        
        <div class="ticker-group" id="tickers"></div>
        
        <div id="risk" class="risk-box"></div>
        <div id="alerts" class="alert-box"></div>
    </div>

    <script>
        async function fetchCoreData() {
            try {
                const res = await fetch('/data.json?t=' + Date.now(), { cache: 'no-store' });
                const data = await res.json();
                
                document.getElementById('timestamp').innerText = `WIRE: ${data.wire} | TIMESTAMP: ${data.timestamp}`;
                
                let htmlTickers = '';
                for (const [key, val] of Object.entries(data.equities || {})) {
                    let extra = '';
                    if (val.change_1m !== undefined) extra += ` (1M: ${val.change_1m}%)`;
                    htmlTickers += `<div class="ticker"><strong>${key}:</strong> <span class="val">$${val.last}</span>${extra}</div>`;
                }
                document.getElementById('tickers').innerHTML = htmlTickers;

                if (data.risk) {
                    document.getElementById('risk').innerHTML = `<strong>RIESGO:</strong> Modo ${data.risk.mode} | Lock: ${data.risk.lock} | Dry Powder: ${data.risk.dry_powder}`;
                }

                if (data.alerts && data.alerts.length > 0) {
                    document.getElementById('alerts').innerHTML = `<strong>ALERTA:</strong> ${data.alerts.join(' | ')}`;
                }
            } catch (e) {
                console.error("Error conectando a Bus Local", e);
            }
        }
        fetchCoreData();
        setInterval(fetchCoreData, 60000);
    </script>
</body>
</html>
HTML

echo "=== [3/5] Creando Bus Central Atomizado (m82_bus.py) ==="
cat > ~/M82/m82_bus.py << 'PYTHON'
import os
import json
import time
import urllib.request

DATA_PATH = os.path.expanduser("~/M82/app/data.json")
BOT_WEBHOOK = os.environ.get("M82_BOT_WEBHOOK", "")
NVFT_WEBHOOK = os.environ.get("M82_NVFT_WEBHOOK", "")

def broadcast(payload):
    tmp = DATA_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, DATA_PATH)
    print(f"[BUS] data.json actualizado: {payload.get('equities', {})}")

    if BOT_WEBHOOK:
        try:
            req = urllib.request.Request(BOT_WEBHOOK, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=5)
            print("[BUS] -> Bot OK")
        except Exception as e:
            print(f"[BUS] Bot fail: {e}")

    if NVFT_WEBHOOK:
        try:
            req = urllib.request.Request(NVFT_WEBHOOK, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=5)
            print("[BUS] -> NVFT OK")
        except Exception as e:
            print(f"[BUS] NVFT fail: {e}")

if __name__ == "__main__":
    while True:
        payload = {
            "source": "M82 Data Core",
            "wire": "M82 Sovereign Wire",
            "timestamp": time.strftime("%H:%M:%S VET"),
            "equities": {
                "BRENT": {"last": 97.76},
                "MEREY16": {"last": 93.92},
                "WTI": {"last": 90.67},
                "SPCX": {"last": 134.19, "change_1m": -15.6, "mcap_b": 1085.1, "eps": -1.69}
            },
            "risk": {
                "mode": "BUNKER",
                "lock": "0.30x",
                "dry_powder": "100%"
            },
            "alerts": ["SPCX -15.6% en 1M vs NASDAQ-100 -13.6% - Sell-off tech, no tesis rota"],
            "breaking": "SPCX $134.19 - Perdió $305.6B de market cap en 1 mes"
        }
        broadcast(payload)
        time.sleep(60)
PYTHON

echo "=== [4/5] Matando Procesos Antiguos y Reiniciando Enjambre ==="
pkill -f "http.server 8000" || true
pkill -f "m82_bus.py" || true

cd ~/M82/app
nohup python3 -m http.server 8000 --bind 0.0.0.0 > ~/M82/http.log 2>&1 &
echo "[HTTP] Servidor Web PWA escuchando en puerto 8000"

cd ~/M82
nohup python3 ~/M82/m82_bus.py > ~/M82/bus.log 2>&1 &
echo "[BUS] Daemon m82_bus.py iniciado (Loop 60s)"

echo "=== [5/5] Purga de Seguridad Final y Confirmación ==="
grep -r -l "^NON " ~/M82 --include="*.md" --include="*.txt" --include="*.sh" --include="*.json" --include="*.html" --include="*.py" 2>/dev/null | xargs -r sed -i '/^NON /d'

sleep 2
curl -s http://127.0.0.1:8000/data.json | head -n 20

echo ""
echo "=== DESPLIEGUE EXITOSO: PWA 127.0.0.1:8000 ONLINE ==="
