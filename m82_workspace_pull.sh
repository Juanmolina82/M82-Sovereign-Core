#!/bin/bash
### M82 V63 AGI :: LSEG WORKSPACE PULL - BASH NATIVO
### Charallave L4/L5 Node | CUSTODIA PASIVA 0.30x LOCK

USER_RDP="jmmp@molina82.com"
PASS_RDP="Trader2026****"
# AppKey Oficial Aprobada en Portal Workspace: M82_TERMINAL_CODE
APP_KEY="276eed13054148edae4918e69273c683"

echo "[M82 BASH] Autenticando con Refinitiv RDP (M82_TERMINAL_CODE)..."

# Petición de Token OAuth2 REST
RESPONSE=$(curl -s -X POST "https://api.refinitiv.com/auth/oauth2/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=$USER_RDP&password=$PASS_RDP&client_id=$APP_KEY&scope=tra.RDP&takeExclusiveSignOnControl=true")

TOKEN=$(echo "$RESPONSE" | jq -r '.access_token // empty')

if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo "======================================================="
    echo "✅ [M82 BASH] TOKEN OK: ${TOKEN:0:25}..."
    echo "======================================================="
    
    echo "[M82 BASH] Jalando PRICING SNAPSHOT (.SPX, .VIX, .DXY)..."
    curl -s "https://api.refinitiv.com/data/pricing/snapshot/v1/?universe=.SPX,.VIX,.DXY&fields=TRDPRC_1,CF_LAST" \
      -H "Authorization: Bearer $TOKEN" | jq .
      
    echo -e "=======================================================\n[JALON OK]"
else
    echo "-------------------------------------------------------"
    echo "⚠️ [M82 RDP CLOUD RESPONSE]:"
    echo "$RESPONSE" | jq .
    echo "[M82 STANDBY] Daemon CPI PID 10448 seguro e intacto en memoria."
    echo "-------------------------------------------------------"
fi
