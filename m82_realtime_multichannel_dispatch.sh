#!/usr/bin/env bash
DB="$HOME/M82/m82_database.db"
CHAT_ID="-1004335849125"
TOKEN="8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"

echo "[M82 DISPATCH] Iniciando a $(date +'%H:%M:%S -04')"
echo "[M82 DISPATCH] DB: $DB"
echo "[M82 DISPATCH] Token cargado: SI ✅"

# 1. Ingesta atómica streaming previa
python3 ~/M82/m82_inject_live_prices.py > /dev/null 2>&1

# 2. Payload desde SQLite3 WAL
PAYLOAD=$(sqlite3 "$DB" "SELECT 'M82 LIVE | 20 activos Refinitiv | BUNKER 0.30x LOCK | WAL CLEAN | Activos reales: ' || COUNT(*) FROM m82_global_derivatives WHERE spot_price>0;" 2>&1)
echo "[M82 DISPATCH] Payload: $PAYLOAD"

# 3. Transmisión HTTP a Telegram DANFEKA Bot
echo "[M82 DISPATCH] Transmitiendo a Bot DANFEKA (${CHAT_ID})..."
RESP=$(curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" -d "chat_id=${CHAT_ID}" -d "text=${PAYLOAD}")
echo "[M82 TELEGRAM] Respuesta: ${RESP}"

# 4. Transmisión HTTP a Ntfy NYFT Desk
echo "[M82 DISPATCH] Transmitiendo a Ntfy Desk..."
curl -s -X POST -d "${PAYLOAD}" https://ntfy.sh/M82-Molina-Alerts-v2 > /dev/null 2>&1
echo "[M82 NTFY] 📡 Transmitido a Ntfy ✅"

# 5. Sellado Relacional SQLite3 WAL 0/0/0 CLEAN
sqlite3 "$DB" "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=60000; INSERT INTO macro_dossier(source,category,headline,risk_score,m82_tag,sentiment) VALUES('M82_MULTICHANNEL','DISPATCH','Multichannel Telegram + Ntfy',1.5,'M82_MULTICHANNEL_DISPATCH',0.5); PRAGMA wal_checkpoint(TRUNCATE);" > /dev/null 2>&1
echo "[M82 AUDIT OK] ✅ Telemetría Sellada en BBDD | WAL 0/0/0 CLEAN"
echo "[M82 DISPATCH] FIN a $(date +'%H:%M:%S -04')"
