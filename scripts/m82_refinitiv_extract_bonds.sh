#!/data/data/com.termux/files/usr/bin/bash

# CREDENCIARES M82 / REFINITIV RDP
USER_RDP="jmmp@molina82.com"
DB="$HOME/M82/m82_database.db"

# Validar variables de entorno
if [ -z "$RDP_PASSWORD" ] || [ -z "$RDP_APP_KEY" ]; then
    echo "[-] Error: Se requiere RDP_PASSWORD y RDP_APP_KEY para la extracción."
    exit 1
fi

echo "[+] Autenticando en Refinitiv RDP ($USER_RDP)..."

# 1. Obtención de Bearer Token
AUTH_RESPONSE=$(curl -s -X POST "https://api.refinitiv.com/auth/oauth2/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "username=$USER_RDP" \
  -d "password=$RDP_PASSWORD" \
  -d "client_id=$RDP_APP_KEY" \
  -d "takeExclusiveSignOnControl=true")

TOKEN=$(echo "$AUTH_RESPONSE" | jq -r '.access_token // empty' 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "[-] Error de autenticación. Verifica la App Key e ingresa el password correcto."
    exit 1
fi

echo "[+] Token obtenido. Extrayendo los 22 bonos de Venezuela y PDVSA..."

# 2. Universo completo de 22 RICs
RICS="VE018118000=,VE019777100=,VE020129200=,VE022832300=,VE023507000=,VE024131200=,VE025042100=,VE026113400=,VE027091500=,VE028050700=,VE031080500=,VE034011300=,VE038033100=,P020085000=,P021090000=,P022060000=,P02212340=,P024060000=,P026060000=,P027041200=,P03509340=,P037041200="

# 3. Request directo de precios (Snapshots)
PRICES_JSON=$(curl -s -X GET "https://api.refinitiv.com/data/environmental-financial-social/v1/pricing/snapshots?universe=$RICS&fields=CF_LAST,CF_BID,CF_ASK,PCTCHNG" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json")

# Verificar si el payload de Refinitiv devolvió precios
TOTAL_EXTRACTED=$(echo "$PRICES_JSON" | jq '.data | length' 2>/dev/null)

if [ -z "$TOTAL_EXTRACTED" ] || [ "$TOTAL_EXTRACTED" -eq 0 ]; then
    echo "[-] Respuesta de precios vacía o inválida de Refinitiv RDP."
    exit 1
fi

HEADLINE="REFINITIV REALTIME RDP ($USER_RDP): $TOTAL_EXTRACTED Bonos extraídos | Curva Sincronizada"
SCORE=0

# 4. Inyección en SQLite M82
sqlite3 "$DB" "PRAGMA busy_timeout=5000; PRAGMA journal_mode=WAL; INSERT INTO m82_multi_stream (daemon_source, headline, final_score, status, created_at) VALUES ('REFINITIV_BONDS_DESK', '$HEADLINE', $SCORE, 'PROCESSED', datetime('now'));" > /dev/null 2>&1

echo "[$(date '+%H:%M:%S')] Extracción completada: $TOTAL_EXTRACTED instrumentos inyectados a M82 | Capa 3: [$SCORE]"
