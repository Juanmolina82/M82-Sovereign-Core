#!/usr/bin/env bash
set -euo pipefail

chmod 600 ~/.m82_env 2>/dev/null || true
set -a && [ -f ~/.m82_env ] && . ~/.m82_env && set +a
export M82_NTFY_URL="${M82_NTFY_URL:-}"
if [ -z "$M82_NTFY_URL" ] && [ -n "${M82_NTFY_TOPIC:-}" ]; then
  export M82_NTFY_URL="https://ntfy.sh/${M82_NTFY_TOPIC}"
fi

python3 - << 'EOF_SYNC_JSON'
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone

db_path = os.path.expanduser("~/M82/m82_database.db")
md_path = os.path.expanduser("~/M82/docs/M82_MACRO_DOSSIER_MASTER_V605.md")
json_path = os.path.expanduser("~/M82/docs/M82_MASTER_KNOWLEDGE_INDEX.json")
out_summary_path = os.path.expanduser("~/M82/logs/last_cycle_summary.json")

os.makedirs(os.path.dirname(json_path), exist_ok=True)
os.makedirs(os.path.dirname(out_summary_path), exist_ok=True)

md_sha256 = None
if os.path.exists(md_path):
    with open(md_path, "rb") as f:
        md_sha256 = hashlib.sha256(f.read()).hexdigest()

conn = sqlite3.connect(db_path, timeout=60.0)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")

vectors = [dict(r) for r in conn.execute("SELECT * FROM macro_dossier ORDER BY rowid ASC").fetchall()]
raw_seals = [dict(r) for r in conn.execute("SELECT * FROM m82_ledger_seals_v2 ORDER BY rowid ASC").fetchall()]

seals = []
for idx, s in enumerate(raw_seals, start=1):
    item = dict(s)
    sid = item.get("seal_id")
    if sid is None:
        sid = item.get("id")
    item["seal_id_resolved"] = sid if sid is not None else idx
    item["prev_hash"] = item.get("prev_hash") or ""
    item["payload_hash"] = item.get("payload_hash") or ""
    seals.append(item)

ts_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
latest_seal = seals[-1] if seals else {}

index_payload = {
    "system": "M82_SOVEREIGN_CORE",
    "version": "v60.5",
    "workspace_user": "jmmp@molina82.com",
    "origin_topology": "CHARALLAVE-L4L5-EDGE <-> CARACAS-HQ-CENTRAL",
    "generated_at_utc": ts_utc,
    "governance_state": {
        "mode": "BUNKER_MODE_CUSTODIA_PASIVA_030X_LOCK",
        "lockout": "NO_TRADE",
        "active_exposure_nav": 0.22,
        "max_exposure_cap": 0.30,
        "dry_powder_pct": 78.0,
        "daily_var_pct": 1.68,
        "warsh_spread_bps": 102.0,
    },
    "artifacts": {
        "master_dossier_md": md_path,
        "master_dossier_sha256": md_sha256,
        "sqlite_db": db_path,
    },
    "ledger_integrity": {
        "total_vectors": len(vectors),
        "total_seals": len(seals),
        "latest_seal_id": latest_seal.get("seal_id_resolved"),
        "latest_payload_hash": latest_seal.get("payload_hash") or None,
    },
    "cryptographic_seals": seals,
    "macro_vectors": vectors,
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(index_payload, f, indent=2, ensure_ascii=False)

with open(json_path, "rb") as f:
    json_sha256 = hashlib.sha256(f.read()).hexdigest()

conn.execute("PRAGMA wal_checkpoint(PASSIVE);")
conn.close()

summary = {
    "ts_utc": ts_utc,
    "vectors": len(vectors),
    "seals": len(seals),
    "json_sha256": json_sha256,
    "json_sha16": json_sha256[:16],
}
with open(out_summary_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(f"[OK] Index sincronizado | vectores={len(vectors)} | sellos={len(seals)} | sha256={json_sha256[:16]}...")
EOF_SYNC_JSON

python3 - << 'EOF_DISPATCH_CYCLE'
import json
import os
import urllib.error
import urllib.parse
import urllib.request

summary_path = os.path.expanduser("~/M82/logs/last_cycle_summary.json")
with open(summary_path, "r", encoding="utf-8") as f:
    s = json.load(f)

MSG = (
    "M82 CICLO SYNC :: MACRO DOSSIER & INDEX\n"
    "Nodo: Charallave L4/L5 Edge x Caracas HQ Central\n"
    "Gob: BUNKER MODE 0.30x LOCK | LOCKOUT: NO TRADE\n"
    "Cartera: 0.22x NAV | Dry Powder 78.0% | VaR ~1.68%\n\n"
    f"- Vectores WAL: {s['vectors']} | Sellos Encadenados: {s['seals']}\n"
    f"- Index SHA-256: {s['json_sha16']}...\n"
    "- Cohorte IA/Neocloud ($CRWV / $NBIS / $IREN): Monitoreo activo sin alterar custodia."
)

bot_token = os.environ.get("M82_BOT_TOKEN", "").strip()
chat_id = os.environ.get("M82_PRIVATE_CHAT_ID", "").strip()
ntfy_url = os.environ.get("M82_NTFY_URL", "").strip()
ntfy_token = os.environ.get("M82_NTFY_TOKEN", "").strip()

if bot_token and chat_id:
    tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": MSG}).encode("utf-8")
    req = urllib.request.Request(tg_url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print("PRIVATE_BOT_HTTP:", r.status)
    except urllib.error.HTTPError as e:
        print(f"PRIVATE_BOT_ERR: {e.code} {e.reason} | BODY: {e.read().decode('utf-8', errors='replace')}")
else:
    print("PRIVATE_BOT_SKIPPED: defina M82_BOT_TOKEN y M82_PRIVATE_CHAT_ID en ~/.m82_env")

if ntfy_url:
    headers = {
        "Title": "M82 Ciclo Sync - Index WAL & Peers ($CRWV/$NBIS/$IREN)",
        "Priority": "default",
        "Tags": "arrows_counterclockwise,file_folder,shield",
    }
    if ntfy_token:
        headers["Authorization"] = f"Bearer {ntfy_token}"
    req_ntfy = urllib.request.Request(ntfy_url, data=MSG.encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req_ntfy, timeout=15) as r2:
            print("NTFY_HTTP:", r2.status, "| URL:", ntfy_url)
    except urllib.error.HTTPError as e:
        print(f"NTFY_HTTP_ERR: {e.code} {e.reason} | URL: {ntfy_url} | BODY: {e.read().decode('utf-8', errors='replace')}")
else:
    print("NTFY_SKIPPED: defina M82_NTFY_URL o M82_NTFY_TOPIC en ~/.m82_env")
EOF_DISPATCH_CYCLE
