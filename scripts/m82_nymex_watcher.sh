#!/data/data/com.termux/files/usr/bin/bash
# M82 V60 AGI :: SERVICE ALERT WATCHER (ALERW29)
# Node: Caracas L4/L5

M82_DIR="$HOME/M82"
VAULT_PATH="$M82_DIR/vault/protected/vault.json"
NTFY_URL="https://ntfy.sh/M82-Molina-Alerts-v4"

echo "[M82] Centinela ALERW29 (NYMEX) activado en segundo plano..."

while true; do
    if [ -f "$VAULT_PATH" ]; then
        LSEG_CLIENT_ID=$(jq -r '.LSEG_APP_KEY_PRIMARY // empty' "$VAULT_PATH")
    fi
    LSEG_CLIENT_ID="${LSEG_CLIENT_ID:-a404050A11740359473F5E70042D524581e}"

    # Obtener token
    TOKEN=$(curl -s -X POST "https://api.refinitiv.com/auth/oauth2/v1/token" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "grant_type=client_credentials&client_id=$LSEG_CLIENT_ID&scope=tra.RDP" | jq -r '.access_token // empty')

    if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
        # Buscar estado de la alerta ALERW29
        CHECK_RESP=$(curl -s -X POST "https://api.refinitiv.com/data/news/v1/stories/search" \
          -H "Authorization: Bearer $TOKEN" \
          -H "Content-Type: application/json" \
          -d '{"query":"ALERW29 AND (CLEAR OR CLEARED OR RECTIFIED)", "count":1}')

        if echo "$CHECK_RESP" | grep -iqE "CLEAR|CLEARED|RECTIFIED"; then
            MSG="🚨 #M82 #ALERT :: LSEG ALERW29 CLEARED — NYMEX Data Feed Restored. Energy Desk Unfrozen."
            
            # Dispatch ntfy + SQLite Log
            curl -s -d "$MSG" "$NTFY_URL" > /dev/null
            sqlite3 "$M82_DIR/m82_database.db" "INSERT INTO m82_multi_stream (daemon_source, headline, status) VALUES ('SERVICE_ALERT', '[M82] LSEG ALERW29 NYMEX CLEAR', 'PENDING');"
            
            echo "🟢 [M82] NYMEX CLEAR DETECTADO. Notificación despachada."
            break
        fi
    fi
    sleep 60
done
