#!/usr/bin/env python3
import os
import sqlite3
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
TABS = ["FRONT_PAGE", "TOP_NEWS", "TRENDING_TOPICS", "LATEST_NEWS", "COMPANIES", "MOST_READ"]

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=60000;")
    conn.row_factory = sqlite3.Row
    return conn

def map_tab(src, hdl):
    s = f"{src} {hdl}".upper()
    if any(k in s for k in ["NVDA", "MSFT", "JPM", "XLK", "COIN", "RTX", "RIO", "COMPANY"]):
        return "COMPANIES"
    if any(k in s for k in ["AI", "WARSH", "FED", "OPEC", "HORMUZ", "TREND"]):
        return "TRENDING_TOPICS"
    if any(k in s for k in ["TOP", "ALERT", "CRITICAL", "BUNKER", "DOSSIER"]):
        return "TOP_NEWS"
    if any(k in s for k in ["MOST", "RANK", "ALPHA"]):
        return "MOST_READ"
    return "LATEST_NEWS"

@app.after_request
def add_cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type"
    r.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return r

@app.route("/health")
def health():
    conn = get_db()
    cur = conn.cursor()
    daemons = cur.execute("SELECT COUNT(*) FROM m82_daemons_registry").fetchone()[0]
    stream_cnt = cur.execute("SELECT COUNT(*) FROM m82_multi_stream").fetchone()[0]
    conn.close()
    return jsonify({
        "status": "ONLINE",
        "port": 8286,
        "node": "CHARALLAVE_L4_L5_EDGE",
        "governance": "BUNKER_MODE_0.30x_LOCK",
        "exposure": "0.22x",
        "var_95_daily": "1.68%",
        "warsh_spread_bps": 102.0,
        "registered_daemons": daemons,
        "stream_events": stream_cnt
    })

@app.route("/api/workspace/tabs")
def workspace_tabs():
    tab = request.args.get("tab", "FRONT_PAGE").upper()
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute("SELECT id, daemon_source, headline, status, created_at FROM m82_multi_stream ORDER BY id DESC LIMIT 40").fetchall()
    ws_rows = cur.execute("SELECT id, tab_category, headline, sector_tag, alpha_score, source, created_at FROM m82_workspace_feed ORDER BY id DESC LIMIT 40").fetchall()
    conn.close()

    items = []
    for r in ws_rows:
        if tab == "FRONT_PAGE" or r["tab_category"] == tab:
            items.append({"id": f"WS-{r['id']}", "tab": r["tab_category"], "source": r["source"], "sector": r["sector_tag"], "headline": r["headline"], "timestamp": r["created_at"]})
    for r in rows:
        mapped = map_tab(r["daemon_source"] or "", r["headline"] or "")
        if tab == "FRONT_PAGE" or mapped == tab:
            items.append({"id": f"MS-{r['id']}", "tab": mapped, "source": r["daemon_source"], "sector": r["status"] or "LIVE", "headline": r["headline"], "timestamp": r["created_at"]})
    return jsonify({"port": 8286, "active_tab": tab, "available_tabs": TABS, "count": len(items), "items": items[:30]})

@app.route("/api/workspace/ingest", methods=["POST"])
def ingest_headline():
    data = request.get_json(force=True, silent=True) or {}
    tab = data.get("tab", "TOP_NEWS").upper()
    if tab not in TABS:
        tab = "FRONT_PAGE"
    headline = data.get("headline", "").strip()
    if not headline:
        return jsonify({"error": "headline requerido"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO m82_workspace_feed (tab_category, headline, sector_tag, alpha_score) VALUES (?, ?, ?, ?)",
                (tab, headline, data.get("sector", "LSEG_WIRE").upper(), float(data.get("alpha_score", 0.92))))
    conn.commit()
    conn.close()
    return jsonify({"status": "INGESTED", "tab": tab})

HTML_UI = """<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>M82 App :8286</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#05080e;color:#f1f5f9;font-family:-apple-system,sans-serif;padding:12px}
.hud{background:#09111e;border:1px solid #1e293b;border-radius:12px;padding:14px;margin-bottom:12px}
.top{display:flex;justify-content:space-between;align-items:center}
.brand{color:#00e5ff;font-weight:800;font-size:15px}
.badge{background:#0f291e;color:#10b981;border:1px solid #059669;padding:3px 8px;border-radius:6px;font-size:11px;font-weight:700}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px;font-size:11px;color:#94a3b8}
.metrics strong{color:#38bdf8;display:block;font-size:13px}
.tabs{display:flex;overflow-x:auto;gap:6px;padding-bottom:8px;margin-bottom:10px}
.tab-btn{background:#0d1522;color:#94a3b8;border:1px solid #1e293b;padding:8px 12px;border-radius:8px;font-size:12px;font-weight:700;white-space:nowrap}
.tab-btn.active{background:#0284c7;color:#fff;border-color:#38bdf8}
.card{background:#090e17;border:1px solid #172033;border-left:3px solid #00e5ff;border-radius:10px;padding:14px;margin-bottom:10px}
.meta{display:flex;justify-content:space-between;font-size:11px;color:#38bdf8;font-weight:700;margin-bottom:6px}
.title{font-size:15px;line-height:1.45;font-weight:600}
.foot{margin-top:8px;font-size:11px;color:#64748b;display:flex;justify-content:space-between}
</style></head><body>
<div class="hud"><div class="top"><div class="brand">M82 APP // WORKSPACE :8286</div><div class="badge">0.30x LOCK</div></div>
<div class="metrics"><span>EXP<strong>0.22x</strong></span><span>VaR<strong>1.68%</strong></span><span>WARSH<strong>+102bps</strong></span></div></div>
<div class="tabs">
<button class="tab-btn active" onclick="st('FRONT_PAGE',this)">Front Page</button>
<button class="tab-btn" onclick="st('TOP_NEWS',this)">Top News</button>
<button class="tab-btn" onclick="st('TRENDING_TOPICS',this)">Trending Topics</button>
<button class="tab-btn" onclick="st('LATEST_NEWS',this)">Latest News</button>
<button class="tab-btn" onclick="st('COMPANIES',this)">Companies</button>
<button class="tab-btn" onclick="st('MOST_READ',this)">Most Read Stories</button>
</div><div id="feed">Cargando :8286...</div>
<script>
let ct='FRONT_PAGE';
function st(t,el){ct=t;document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));el.classList.add('active');lf();}
async function lf(){try{const r=await fetch('/api/workspace/tabs?tab='+ct);const d=await r.json();
document.getElementById('feed').innerHTML=d.items.length?d.items.map(i=>`<div class="card"><div class="meta"><span>${i.tab} // ${i.source}</span><span>${i.sector}</span></div><div class="title">${i.headline}</div><div class="foot"><span>${i.id}</span><span>${i.timestamp||'LIVE'}</span></div></div>`).join(''):'<div class="card"><div class="title">Esperando flujo LSEG...</div></div>';}catch(e){}}
setInterval(lf,5000);lf();
</script></body></html>"""

@app.route("/")
def index():
    return render_template_string(HTML_UI)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8286, debug=False)
