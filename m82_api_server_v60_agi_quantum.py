#!/usr/bin/env python3
import os, sqlite3, json, time, math
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    return conn

@app.route('/health')
@app.route('/api/status')
def status():
    return jsonify({
        "status": "ONLINE",
        "governance": "🔒 BUNKER MODE",
        "lock": "0.30x",
        "var": "1.68%",
        "warsh": "+102bps",
        "node": "Charallave L4/L5 Sovereign Edge",
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "AGI QUANTUM + BIG DATA + CUSTODIA PASIVA"
    })

@app.route('/api/stream')
def stream():
    try:
        conn = get_db()
        cur = conn.cursor()
        rows = cur.execute("""
            SELECT daemon_source, headline, status, alpha_score, asset_impact, sentiment, created_at 
            FROM m82_multi_stream ORDER BY id DESC LIMIT 50
        """).fetchall()
        conn.close()
        
        data = []
        for r in rows:
            d = dict(r)
            alpha = d.get('alpha_score') or 0.85
            sentiment = d.get('sentiment') or 0.5
            quant_signal = round(alpha * 0.7 + sentiment * 0.3 + math.sin(time.time()/100)*0.05, 4)
            var_contrib = round((1 - alpha) * 1.68, 4)
            
            d['quant_signal'] = quant_signal
            d['var_contrib'] = var_contrib
            d['agi_tag'] = "QUANTUM_ENTANGLED" if quant_signal > 0.8 else "BIG_DATA_INGEST"
            data.append(d)
            
        return jsonify({"stream": data, "count": len(data), "engine": "AGI QUANTUM V60"})
    except Exception as e:
        return jsonify({"stream": [], "count": 0, "error": str(e)})

@app.route('/api/hud_card', methods=['POST'])
def hud():
    payload = request.json or {}
    return jsonify({"status": "HUD DISPARADA", "payload": payload, "mode": "AGI QUANTUM HUD"})

if __name__ == '__main__':
    from waitress import serve
    print("🟢 M82 AGI QUANTUM TERMINAL — Waitress WSGI :8083 ONLINE")
    serve(app, host='0.0.0.0', port=8083, threads=16)
