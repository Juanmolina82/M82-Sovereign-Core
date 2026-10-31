#!/usr/bin/env bash
set -e

# Reemplaza con el token activo actual de @BotFather
NEW_TOKEN="8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID="-1004335849125"

python3 -c "
import os, re
for f in ['orch.py', 'm82_refinitiv_realtime_bridge.py', 'm82_master_dossier.py']:
    path = os.path.expanduser(f'~/M82/{f}')
    if os.path.exists(path):
        with open(path, 'r') as fp:
            content = fp.read()
        content = re.sub(r'TOKEN\s*=\s*[\"'].*?[\"']', f'TOKEN = \"{NEW_TOKEN}\"', content)
        with open(path, 'w') as fp:
            fp.write(content)
        print(f'✅ {f} actualizado con nuevo token.')
"

# Probar despacho directo
curl -s -X POST "https://api.telegram.org/bot${NEW_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  -d "text=⚡ *#M82 FREIGHT STRESS EXECUTION CONFIRMED* %0AScenario: Bab-el-Mandeb Block %0AVaR: 1.68% | Lock: 0.30x %0AStatus: WAL 0/0/0 OK" \
  -d "parse_mode=Markdown" | grep -o '"ok":true' && echo " -> Dispatch 200 OK"
