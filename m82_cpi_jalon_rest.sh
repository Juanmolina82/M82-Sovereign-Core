#!/bin/bash
### M82 V63 AGI :: LSEG RDP REST PULL CANÓNICO (NO SDK / NO LOCALHOST)
### Charallave L4/L5 Node | CUSTODIA PASIVA 0.30x LOCK

USER_RDP="jmmp@molina82.com"
PASS_RDP="Trader2026****"
APP_KEY="374da013581c4eebd9276922248ade81e285d0d6" # M82_TERMUX_CORE / Vault Primary

echo "[M82 REST] Solicitando Token OAuth2 a RDP Cloud..."

# Handshake REST Directo
RESPONSE=$(curl -s -X POST "https://api.refinitiv.com/auth/oauth2/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=$USER_RDP&password=$PASS_RDP&client_id=$APP_KEY&scope=tra.RDP&takeExclusiveSignOnControl=true")

TOKEN=$(echo "$RESPONSE" | jq -r '.access_token // empty')

if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo "======================================================="
    echo "✅ [M82 REST] PLATFORM SESSION ACTIVE: ${TOKEN:0:25}..."
    echo "======================================================="
    
    echo "[M82 REST] Ingestando matriz de precios macro (.SPX, .VIX, .DXY, US10YT=RR)..."
    
    # Snapshot de precios puro
    curl -s "https://api.refinitiv.com/data/pricing/snapshot/v1/?universe=.SPX,.VIX,.DXY,US10YT=RR&fields=TRDPRC_1,CF_LAST,HIGH_1,LOW_1" \
      -H "Authorization: Bearer $TOKEN" | jq .
      
    echo -e "=======================================================\n[CPI REST PULL OK]"
else
    echo "-------------------------------------------------------"
    echo "⚠️ [M82 RDP FALLBACK RESPONSE]:"
    echo "$RESPONSE" | jq .
    echo "[M82 STANDBY] El daemon CPI PID 10448 permanece resguardado e intacto."
    echo "-------------------------------------------------------"
fi
