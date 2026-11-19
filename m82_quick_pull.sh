#!/bin/bash
USER_RDP="jmmp@molina82.com"
PASS_RDP="Trader2026****"
APP_KEY="374da013581c4eebd9276922248ade81e285d0d6"
TOKEN_FILE="$HOME/M82/.token"

# 1. Obtener Token OAuth2 válido
echo "🟢 [M82 REST] Validando Token en $TOKEN_FILE..."
RESPONSE=$(curl -s -X POST "https://api.refinitiv.com/auth/oauth2/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=$USER_RDP&password=$PASS_RDP&client_id=$APP_KEY&scope=tra.RDP&takeExclusiveSignOnControl=true")

TOKEN=$(echo "$RESPONSE" | jq -r '.access_token // empty')

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
    echo "⚠️ Fallo Password Grant. Probando Client Credentials..."
    RESPONSE=$(curl -s -X POST "https://api.refinitiv.com/auth/oauth2/v1/token" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "grant_type=client_credentials&client_id=$APP_KEY&scope=tra.RDP")
    TOKEN=$(echo "$RESPONSE" | jq -r '.access_token // empty')
fi

if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo "$TOKEN" > "$TOKEN_FILE"
    echo "✅ Token Activo: ${TOKEN:0:25}..."
    AUTH="Authorization: Bearer $TOKEN"

    echo -e "\n======================================================="
    echo "📊 1. MERCADO EN VIVO (PRECIOS & MACRO ENTITLED)"
    echo "======================================================="
    curl -s "https://api.refinitiv.com/data/pricing/snapshot/v1/?universe=.SPX,.VIX,.DXY,US10YT=RR,ESc1,CLc1,GCc1,NVDA.O,JPM.N" \
      -H "$AUTH" > /tmp/market_temp.json
    jq '.' /tmp/market_temp.json | head -40

    echo -e "\n======================================================="
    echo "📰 2. REUTERS WIRE (VENEZUELA OR ENERGY OR CPI)"
    echo "======================================================="
    curl -s -X POST "https://api.refinitiv.com/data/news/v1/stories/search" \
      -H "$AUTH" \
      -H "Content-Type: application/json" \
      -d '{"query": "Venezuela OR ENERGY OR CPI", "sort": "date desc", "count": 10}' > /tmp/wire_temp.json

    jq '.stories[]? | {time:.versionCreated, headline:.title.text}' /tmp/wire_temp.json

    # 3. Guardado en SQLite WAL
    python3 -c "
import json, sqlite3, os
db_path = os.path.expanduser('~/M82/m82_database.db')
if os.path.exists(db_path) and os.path.exists('/tmp/wire_temp.json'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('PRAGMA busy_timeout=60000;')
    try:
        data = json.load(open('/tmp/wire_temp.json'))
        stories = data.get('stories', [])
        count = 0
        for s in stories:
            hl = '[LSEG REST] ' + str(s.get('title', {}).get('text', ''))
            try:
                c.execute(\"INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status) VALUES ('LSEG_REST_MANUAL', ?, 'PENDING')\", (hl,))
                count += 1
            except Exception: pass
        conn.commit()
        print('🟢 Inyectados ' + str(count) + ' titulares en m82_database.db')
    except Exception as e:
        print('⚠️ Error al procesar Wire JSON: ' + str(e))
    conn.close()
"
else
    echo "⚠️ Fallo de Autenticación RDP. Salida recibida:"
    echo "$RESPONSE" | jq .
    echo "[M82 STANDBY] PID 10448 resguardado en memoria."
fi
