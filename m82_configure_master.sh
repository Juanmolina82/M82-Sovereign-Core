#!/bin/bash
# ==============================================================================
# M82 V60.7.0 PRIME :: MASTER ARCHITECTURE INTEGRATION & HARDENING SCRIPT
# Primary Node: Caracas HQ Master Node / Charallave L4 Edge
# Governance: Bunker Mode (0.30x Lock) | Zero-PII Gateway
# ==============================================================================

set -e

M82_DIR="$HOME/M82"
DASH_DIR="$M82_DIR/dashboard"
VAULT_DIR="$M82_DIR/vault/protected"

echo "🏛 [1/5] Verificando y asegurando la estructura de directorios M82..."
mkdir -p "$M82_DIR" "$DASH_DIR" "$VAULT_DIR" "$M82_DIR/desks" "$HOME/M82_BACKUPS"

echo "💾 [2/5] Hardening de la Base de Datos Principal (SQLite WAL Mode)..."
python3 -c "
import sqlite3, os
db_path = os.path.expanduser('~/M82/m82_database.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('PRAGMA journal_mode=WAL;')
c.execute('PRAGMA synchronous=NORMAL;')
c.execute('PRAGMA busy_timeout=60000;')
conn.commit()
conn.close()
print('  ✅ PRAGMAs WAL, synchronous=NORMAL y busy_timeout=60000 asegurados.')
"

echo "🤖 [3/5] Integrando el Notificador Ligero de Daemons (D-61)..."
cat << 'PYEOF' > "$M82_DIR/m82_daemon_notifier.py"
#!/usr/bin/env python3
# ==============================================================================
# M82 V60.7.0 PRIME :: MACRO DOSSIER DAEMON NOTIFIER ENGINE (D-61 INTEGRATION)
# ==============================================================================

import os, sqlite3, json, urllib.request, urllib.error

BOT_TOKEN = "8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4"
CHAT_ID = "-1004335849125"

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
LAST_ID_FILE = os.path.expanduser("~/M82/.last_notified_id")

def send_telegram_alert(message_html):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message_html,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            return res.get("ok", False)
    except Exception as e:
        return False

def check_and_notify_daemons():
    if not os.path.exists(DB_PATH):
        return

    last_id = 0
    if os.path.exists(LAST_ID_FILE):
        try:
            with open(LAST_ID_FILE, "r") as f:
                last_id = int(f.read().strip())
        except ValueError:
            last_id = 0

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, daemon_source, headline, desk, alpha_score, created_at 
        FROM m82_multi_stream 
        WHERE id > ? AND status='VERIFIED'
        ORDER BY id ASC LIMIT 5
    """, (last_id,))
    
    new_events = c.fetchall()
    
    if not new_events:
        conn.close()
        return

    new_last_id = last_id
    for event_id, source, headline, desk, alpha, ts in new_events:
        new_last_id = max(new_last_id, event_id)
        
        msg_html = f"""🤖 <b>#M82 DAEMON ALERT :: [{desk}]</b>
🏛 <b>Node:</b> Caracas HQ Master Node
🛰 <b>Daemon Source:</b> <code>{source}</code>
⏱ <b>Timestamp:</b> <code>{ts}</code>

📰 <b>Event Payload:</b>
{headline}

📊 <b>Alpha Score:</b> <code>{alpha}</code> | <b>Status:</b> <code>VERIFIED</code>
🔒 <i>Zero-PII Gateway Protected</i>"""

        send_telegram_alert(msg_html)

    conn.close()

    with open(LAST_ID_FILE, "w") as f:
        f.write(str(new_last_id))

if __name__ == "__main__":
    check_and_notify_daemons()
PYEOF

chmod +x "$M82_DIR/m82_daemon_notifier.py"

echo "⏱ [4/5] Actualizando el Orquestador Dual Cron (08:00 / 16:00 VET + Daemon Notifier)..."
cat << 'SHEOF' > "$M82_DIR/m82_cron_runner.sh"
#!/bin/bash
# M82 V60.7.0 PRIME DUAL CRON ORCHESTRATOR + DAEMON NOTIFIER DISPATCH

termux-wake-lock

LAST_PUSH=""

while true; do
  CURRENT_TIME=$(date +"%H:%M")
  
  # 1. Bucle continuo de daemons, rebuild de UI y despacho de alertas
  python3 ~/M82/m82_macro200_grid_deploy.py > /dev/null 2>&1 || true
  python3 ~/M82/m82_caracas_dashboard_v6033_builder.py > /dev/null 2>&1 || true
  python3 ~/M82/m82_daemon_notifier.py > /dev/null 2>&1 || true
  
  # 2. Auto-push 08:00 VET (Apertura)
  if [ "$CURRENT_TIME" == "08:00" ] && [ "$LAST_PUSH" != "08:00" ]; then
    bash ~/M82/m82_daily_0800_scheduler.sh > /dev/null 2>&1 || true
    python3 -c "import sys; sys.path.append('$HOME/M82'); from m82_private_bot import dispatch_executive_summary; dispatch_executive_summary('MORNING OPENING DISPATCH')" > /dev/null 2>&1 || true
    LAST_PUSH="08:00"
  fi

  # 3. Auto-push 16:00 VET (Cierre)
  if [ "$CURRENT_TIME" == "16:00" ] && [ "$LAST_PUSH" != "16:00" ]; then
    python3 ~/M82/m82_lpl_daily_reporter.py > /dev/null 2>&1 || true
    python3 -c "import sys; sys.path.append('$HOME/M82'); from m82_private_bot import dispatch_executive_summary; dispatch_executive_summary('MARKET CLOSE DISPATCH')" > /dev/null 2>&1 || true
    LAST_PUSH="16:00"
  fi

  sleep 300
done
SHEOF

chmod +x "$M82_DIR/m82_cron_runner.sh"

echo "🛡 [5/5] Re-inicializando demonio de fondo y registrando evento de gobernanza..."
pkill -9 -f "m82_cron_runner.sh" || true
nohup bash "$M82_DIR/m82_cron_runner.sh" > "$M82_DIR/cron_prime.log" 2>&1 &

sqlite3 "$M82_DIR/m82_database.db" << 'SQL'
PRAGMA busy_timeout=60000;
INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
  'SYSTEM_GOVERNANCE',
  '[INFRASTRUCTURE HARDENED V60.7.0] Core Architecture Hardened | Daemon Notifier D-61 Linked | Cron Active',
  'VERIFIED',
  1.00,
  'SYSTEM_WIDE'
);
SQL

echo ""
echo "=============================================================================="
echo " ✅ M82 MASTER ARCHITECTURE FULLY CONFIGURED & HARDENED (V60.7.0 PRIME)"
echo " • Engine       : SQLite3 WAL Mode (busy_timeout=60000)"
echo " • Orchestrator : Dual Cron (08:00 / 16:00 VET) + Daemon Notifier"
echo " • Bot Channel  : Telegram Private (-1004335849125)"
echo " • Lock Status  : 🔒 ACTIVE (0.30x LOCK — BUNKER MODE)"
echo "=============================================================================="
