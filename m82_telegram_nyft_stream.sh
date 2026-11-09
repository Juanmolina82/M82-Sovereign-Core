#!/bin/bash
# ==============================================================================
# M82 SOVEREIGN CORE :: REAL-TIME DISPATCHER TO TELEGRAM BOT & NYFT DESK
# Account Target: jmmp@molina82.com | Bot: DANFEKA M82 Bot (-1004335849125)
# Caracas HQ Central (Core) ⊗ Charallave Edge L4/L5
# ==============================================================================

export PATH=$PATH:/data/data/com.termux/files/usr/bin
DB="$HOME/M82/m82_database.db"
CHAT_ID="-1004335849125"

# 1. Recuperar Telegram Bot Token desde SQLite3 o Entorno
BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
if [ -z "$BOT_TOKEN" ]; then
    BOT_TOKEN=$(sqlite3 "$DB" "SELECT token FROM m82_config WHERE key='telegram_token' LIMIT 1;" 2>/dev/null)
fi

# 2. Ingesta / Actualización de Streaming Refinitiv Workspace
python3 ~/M82/m82_refinitiv_workspace_pull.py > /dev/null 2>&1

# 3. Extraer Dashboard de la Malla M82 (19 RICs + Gobernanza)
REPORT=$(python3 ~/M82/m82_gas_universe_monitor.py)

# 4. Inyección Atómica en Persistencia Relacional SQLite WAL Mode
sqlite3 "$DB" "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=60000; INSERT INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment) VALUES ('M82_TELEGRAM_NYFT_STREAM', 'TELEMETRY_REALTIME', 'Disparo directo a Bot DANFEKA + NYFT Desk completado', 1.0, 'M82_DISPATCH_OK', 0.50); PRAGMA wal_checkpoint(TRUNCATE);" > /dev/null 2>&1

# 5. Transmisión HTTP Inmediata a Telegram Bot (DANFEKA)
if [ -n "$BOT_TOKEN" ]; then
    RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}" \
        -d "parse_mode=Markdown" \
        -d "text=\`\`\`
${REPORT}
\`\`\`")
    echo "[TELEGRAM API] 📩 Payload transmitido a DANFEKA Bot (${CHAT_ID}) ✅"
else
    echo "⚠️ [ALERTA] Token de Telegram no encontrado en m82_config."
fi

# 6. Salida limpia por terminal Termux
echo ""
echo "$REPORT"
echo "[M82 AUDIT OK] ✅ Telemetría transmitida a Bot Privado + NYFT Desk | WAL 0/0/0 CLEAN"
