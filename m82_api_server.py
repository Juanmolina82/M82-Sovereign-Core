#!/usr/bin/env python3
import os, sqlite3, json
from flask import Flask, jsonify, send_from_directory
app=Flask(__name__, static_folder=os.path.expanduser('~/M82'))
DB=os.path.expanduser("~/M82/m82_database.db")
def get_db():
    conn=sqlite3.connect(DB); conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;"); conn.execute("PRAGMA busy_timeout=60000;")
    return conn
@app.route('/')
def idx(): return send_from_directory(os.path.expanduser('~/M82'),'index.html')
@app.route('/health')
def health():
    conn=get_db(); cur=conn.cursor()
    cur.execute("SELECT COUNT(*) as c FROM m82_daemons_registry")
    daemons=cur.fetchone()['c'] if cur else 0
    conn.close()
    return jsonify({"status":"ONLINE","node":"SOVEREIGN EXECUTION CORE","daemons":daemons,"governance":"BUNKER_030X","var":"1.68%","exposure":"0.22x/0.30x","merey":"$93.75 Sep / $93.92 Live","brent":"$112.92"})
@app.route('/api/stream')
def stream():
    try:
        conn=get_db(); cur=conn.cursor()
        cur.execute("SELECT id, daemon_source, headline, status, created_at FROM m82_multi_stream ORDER BY id DESC LIMIT 30")
        rows=[dict(r) for r in cur.fetchall()]; conn.close()
        return jsonify(rows)
    except Exception as e: return jsonify({"error":str(e)}),500
@app.route('/api/starmine')
def starmine():
    return jsonify({"models":15,"list":["CAM","ARM","EQ","RV","IV","Val-Mo","Price Mo","SH","SI","IF","CCR","SRCR","SCR","TMCR","MATM"],"proprietary":["Recommendation","Target Price","Upside %","Internal Research"]})
if __name__=='__main__':
    from waitress import serve
    print("🚀 M82 API :8083 + WEB :8080 — 100+ DAEMONS — BUNKER 0.30x")
    serve(app, host='0.0.0.0', port=8083)
