#!/bin/bash
### M82 V63 AGI :: LSEG RDP PULL NATIVO BASH (TERMINAL CODE APPKEY)
### Charallave L4/L5 Edge | CUSTODIA PASIVA 0.30x LOCK

USER_RDP="jmmp@molina82.com"
PASS_RDP="Trader2026****"
# AppKey Oficial Aprobada en Portal: M82_TERMINAL_CODE
APP_KEY="276eed13054148edae4918e69273c683"

echo "[M82 BASH] Autenticando con AppKey M82_TERMINAL_CODE..."

# Petición de Token OAuth2 RDP
RESPONSE=$(curl -s -X POST "https://api.refinitiv.com/auth/oauth2/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=$USER_RDP&password=$PASS_RDP&client_id=$APP_KEY&scope=tra.RDP&takeExclusiveSignOnControl=true")

TOKEN=$(echo "$RESPONSE" | jq -r '.access_token // empty')

if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo "======================================================="
    echo "✅ [M82 BASH] TOKEN OK: ${TOKEN:0:25}..."
    echo "======================================================="
    
    echo "[M82 BASH] Jalando cotizaciones continuas (.SPX, .VIX, .DXY)..."
    
    # Snapshot REST de precios
    curl -s "https://api.refinitiv.com/data/pricing/snapshot/v1/?universe=.SPX,.VIX,.DXY&fields=TRDPRC_1,CF_LAST" \
      -H "Authorization: Bearer $TOKEN" | jq .
      
    echo -e "=======================================================\n[JALON OK]"
else
    echo "-------------------------------------------------------"
    echo "⚠️ [M82 RDP RESPONSE]:"
    echo "$RESPONSE" | jq .
    echo "[M82 STANDBY] El daemon CPI PID 10448 se mantiene activo e intacto."
    echo "-------------------------------------------------------"
fi
