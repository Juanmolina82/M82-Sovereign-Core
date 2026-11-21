#!/usr/bin/env python3
"""
M82 UNIFIED SOVEREIGN HUB & REST API SERVER (PORT 8286)
Nodo Charallave Edge L4/L5 — Molina Holdings LLC
"""
import os
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, jsonify, Response

app = Flask(__name__)
DB_PATH = os.path.expanduser("~/M82/m82_database.db")

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

def query_db(query, args=(), one=False):
    if not os.path.exists(DB_PATH):
        return None if one else []
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        rv = cur.fetchall()
    except sqlite3.OperationalError:
        rv = []
    finally:
        conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/health', methods=['GET'])
def health():
    ny_now = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")
    stream_count = query_db("SELECT COUNT(*) as c FROM m82_multi_stream", one=True)
    return jsonify({
        "status": "ONLINE",
        "port": 8286,
        "node": "SOVEREIGN_CHARALLAVE_L4_L5",
        "hq": "CARACAS_HQ_CENTRAL",
        "ny_et_clock": ny_now,
        "governance": "BUNKER_MODE_030X_LOCK",
        "exposure": "0.22x",
        "var_l5": "1.68%",
        "warsh_spread": "+102.0 bps",
        "db_wal_mode": True,
        "stream_records": stream_count["c"] if stream_count else 0
    })

@app.route('/api/stream', methods=['GET'])
def get_stream():
    rows = query_db("SELECT id, daemon_source, headline, status, COALESCE(created_at, timestamp) as ts FROM m82_multi_stream ORDER BY id DESC LIMIT 30")
    data = [dict(r) for r in rows]
    return jsonify({"count": len(data), "stream": data})

@app.route('/api/dossier', methods=['GET'])
def get_dossier():
    rows = query_db("SELECT * FROM macro_dossier ORDER BY id DESC LIMIT 15")
    data = [dict(r) for r in rows]
    return jsonify({"count": len(data), "dossier": data})

@app.route('/', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
def dashboard():
    html = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>M82 SOVEREIGN TERMINAL :8286</title>
<style>
  body { background:#070b12; color:#e2e8f0; font-family:monospace; margin:0; padding:16px; }
  .header { border:1px solid #1e293b; background:#0f172a; padding:16px; border-radius:8px; margin-bottom:16px; }
  .title { color:#38bdf8; font-size:1.2rem; font-weight:bold; margin:0 0 8px 0; }
  .badge { display:inline-block; background:#064e3b; color:#34d399; padding:4px 8px; border-radius:4px; font-size:0.8rem; margin-right:6px; }
  .warn { background:#451a03; color:#fbbf24; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:10px; margin:12px 0; }
  .card { background:#0f172a; border:1px solid #1e293b; padding:12px; border-radius:6px; }
  .label { color:#94a3b8; font-size:0.75rem; }
  .val { color:#f8fafc; font-size:1.1rem; font-weight:bold; margin-top:4px; }
  .feed { background:#0f172a; border:1px solid #1e293b; padding:12px; border-radius:8px; }
  .item { border-bottom:1px solid #1e293b; padding:8px 0; font-size:0.85rem; }
  .src { color:#38bdf8; font-weight:bold; }
</style>
</head>
<body>
  <div class="header">
    <div class="title">🏛️ M82 SOVEREIGN CORE v50 — UNIFIED HUB (:8286)</div>
    <span class="badge">● ONLINE</span>
    <span class="badge warn">BUNKER MODE 0.30x LOCK</span>
    <span class="badge" id="ny-clock">NY ET: --:--:--</span>
  </div>
  <div class="grid">
    <div class="card"><div class="label">NODO OPERATIVO</div><div class="val">CHARALLAVE L4/L5</div></div>
    <div class="card"><div class="label">EXPOSICIÓN ACTIVA</div><div class="val">0.22x</div></div>
    <div class="card"><div class="label">VaR DIARIO (L5)</div><div class="val">1.68%</div></div>
    <div class="card"><div class="label">WARSH SPREAD</div><div class="val">+102.0 bps</div></div>
  </div>
  <div class="feed">
    <div style="color:#38bdf8;font-weight:bold;margin-bottom:8px;">📡 LIVE TELEMETRY STREAM (SQLite WAL)</div>
    <div id="stream-box">Cargando telemetría del enjambre...</div>
  </div>
<script>
async function refreshHub() {
  try {
    const h = await fetch('/health').then(r => r.json());
    document.getElementById('ny-clock').innerText = 'NY ET: ' + h.ny_et_clock;
    const s = await fetch('/api/stream').then(r => r.json());
    const box = document.getElementById('stream-box');
    if (!s.stream || s.stream.length === 0) {
      box.innerHTML = '<div class="item">Enjambre en escucha activa. Sin eventos nuevos en cola.</div>';
      return;
    }
    box.innerHTML = s.stream.map(r =>
      `<div class="item"><span class="src">[${r.daemon_source || 'M82-CORE'}]</span> ${r.headline} <span style="color:#64748b">(${r.ts || ''})</span></div>`
    ).join('');
  } catch (e) { console.error(e); }
}
refreshHub();
setInterval(refreshHub, 5000);
</script>
</body>
</html>"""
    return Response(html, mimetype='text/html')

if __name__ == '__main__':
    from waitress import serve
    print("🚀 [M82 UNIFIED HUB] Dashboard + API REST activos en http://127.0.0.1:8286")
    serve(app, host='0.0.0.0', port=8286, threads=8)
