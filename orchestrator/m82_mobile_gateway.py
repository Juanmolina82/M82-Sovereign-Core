#!/usr/bin/env python3
import os, json, sqlite3, html
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote

ROOT = os.path.expanduser("~/M82")
TOK = open(os.path.join(ROOT, ".env.gateway")).read().strip().split("=")[1]

def state():
    d = {"q": {}, "m": [], "a": []}
    try:
        c1 = sqlite3.connect("file:" + os.path.join(ROOT, "m82_orchestrator_wal.db") + "?mode=ro", uri=True, timeout=30)
        c1.execute("PRAGMA busy_timeout=60000;")
        for r in c1.execute("SELECT payload_json FROM m82_refinitiv_feed_ledger ORDER BY captured_at DESC LIMIT 5").fetchall():
            try: d["q"].update(json.loads(r[0]))
            except Exception: pass
        c1.close()
    except Exception: pass
    try:
        c2 = sqlite3.connect("file:" + os.path.join(ROOT, "m82_database.db") + "?mode=ro", uri=True, timeout=30)
        c2.execute("PRAGMA busy_timeout=60000;")
        tabs = {r[0] for r in c2.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        for t in tabs:
            cols = [col[1] for col in c2.execute(f"PRAGMA table_info({t})").fetchall()]
            if "ticker" in cols and ("latest" in cols or "price" in cols or "value" in cols):
                vcol = "latest" if "latest" in cols else ("price" if "price" in cols else "value")
                for tk, val in c2.execute(f"SELECT ticker, {vcol} FROM {t} ORDER BY rowid DESC LIMIT 30").fetchall():
                    if tk and val is not None: d["q"][str(tk)] = val
            elif "ric" in cols and ("last" in cols or "price" in cols or "value" in cols):
                vcol = "last" if "last" in cols else ("price" if "price" in cols else "value")
                for tk, val in c2.execute(f"SELECT ric, {vcol} FROM {t} ORDER BY rowid DESC LIMIT 30").fetchall():
                    if tk and val is not None: d["q"][str(tk)] = val
        if "macro_dossier" in tabs:
            rows = c2.execute("SELECT id, source, category, headline, risk_score, m82_tag, created_at FROM macro_dossier WHERE headline NOT LIKE '%Live Poll 20 activos%' AND headline NOT LIKE '%Live Pull 20 activos%' AND headline NOT LIKE '%Multichannel Telegram%' ORDER BY id DESC LIMIT 35").fetchall()
            d["m"] = [{"id": r[0], "s": r[1], "c": r[2], "h": r[3], "r": r[4], "t": r[5], "ts": r[6]} for r in rows]
        if "m82_tail_risk_alerts" in tabs:
            rows = c2.execute("SELECT id, event_type, headline, risk_score FROM m82_tail_risk_alerts ORDER BY id DESC LIMIT 12").fetchall()
            d["a"] = [{"id": r[0], "t": r[1], "h": r[2], "r": r[3]} for r in rows]
        c2.close()
    except Exception: pass
    return d

def render_dispatch(item_id):
    title, source, cat, risk, tag, ts, body = "DESPACHO SOBERANO M82", "M82 QUANTUM WIRE", "MACRO_DESK", "N/A", "BUNKER_LOCK", "", ""
    try:
        c2 = sqlite3.connect("file:" + os.path.join(ROOT, "m82_database.db") + "?mode=ro", uri=True, timeout=30)
        c2.execute("PRAGMA busy_timeout=60000;")
        cols = [col[1] for col in c2.execute("PRAGMA table_info(macro_dossier)").fetchall()]
        extra_col = "summary" if "summary" in cols else ("content" if "content" in cols else ("body" if "body" in cols else "headline"))
        if str(item_id).startswith("A-"):
            aid = str(item_id).replace("A-", "")
            row = c2.execute("SELECT event_type, headline, risk_score FROM m82_tail_risk_alerts WHERE id=?", (aid,)).fetchone()
            if row:
                cat, title, risk, source, tag = str(row[0]), str(row[1]), str(row[2]), "M82 Quantum TAIL-RISK", "TAIL_RISK_ALERT"
                body = title
        else:
            q_sql = f"SELECT source, category, headline, risk_score, m82_tag, created_at, {extra_col} FROM macro_dossier " + ("ORDER BY id DESC LIMIT 1" if item_id == "latest" else "WHERE id=?")
            row = c2.execute(q_sql).fetchone() if item_id == "latest" else c2.execute(q_sql, (item_id,)).fetchone()
            if row:
                source, cat, title, risk, tag, ts, body = [str(x or "") for x in row]
        c2.close()
    except Exception as e:
        body = f"Lectura RAM WAL: {e}"
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{background:#07090d;color:#e8f0fe;font-family:sans-serif;margin:0;padding:16px}}.bar{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1e293b;padding-bottom:12px;margin-bottom:16px}}.btn{{background:#001eff;color:#fff;border:none;padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:700;font-size:12px}}.bunker{{background:#2a080d;border:1px solid #ff1744;color:#ff5252;padding:6px 10px;border-radius:4px;font-size:11px;font-weight:700}}.card{{background:#0d1117;border:1px solid #1f2937;border-radius:8px;padding:16px}}.meta{{color:#94a3b8;font-size:12px;margin-bottom:8px;font-family:monospace}}h1{{font-size:18px;line-height:1.4;margin:8px 0 14px;color:#fff}}.body{{font-size:14px;line-height:1.65;color:#cbd5e1;white-space:pre-wrap;border-top:1px solid #1f2937;padding-top:12px}}.tag{{display:inline-block;background:#1e1b4b;color:#a5b4fc;border:1px solid #4338ca;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:700;margin-right:6px}}
.casc-sec{padding:16px 14px 8px;font-size:12px;font-weight:800;color:#60a5fa;text-transform:uppercase;letter-spacing:.7px;background:#07090d}
.casc-list{display:flex;flex-direction:column;background:#0d1117;border-top:1px solid #1e293b;border-bottom:1px solid #1e293b}
.casc-row{display:flex;justify-content:space-between;align-items:center;padding:16px 14px;border-bottom:1px solid #1e293b;font-size:15px;font-weight:700;color:#f8fafc;cursor:pointer;width:100%}
.casc-row:last-child{border-bottom:none}
.casc-row:active{background:#1e293b}
.casc-row small{display:block;font-size:11px;font-weight:500;color:#94a3b8;margin-top:2px}
.pager-bar{display:flex;justify-content:space-between;align-items:center;background:#0b1120;padding:10px 12px;border-bottom:1px solid #1e293b;gap:6px}
.pg-btn{background:#111827;border:1px solid #1f2937;color:#e2e8f0;padding:6px 10px;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer}
.pg-btn.pri{background:#001eff;border-color:#3b82f6;color:#fff}
.pg-mid{font-size:12px;font-weight:800;color:#94a3b8;text-align:center;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
</style></head><body><div class="bar"><a class="btn" href="/">&#8592; Front Page</a><span class="bunker">&#128274; BUNKER 0.30x LOCK</span></div><div class="card"><div class="meta">ID #{html.escape(str(item_id))} &bull; {html.escape(source)} &bull; {html.escape(ts)}</div><div><span class="tag">{html.escape(cat)}</span><span class="tag" style="color:#fbbf24;border-color:#b45309;background:#451a03">RISK {html.escape(risk)}</span><span class="tag">{html.escape(tag)}</span></div><h1>{html.escape(title)}</h1><div class="body">{html.escape(body or title)}</div></div></body></html>"""

HTML = """<!doctype html><html><head><meta charset="utf-8"><link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#001eff"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,sans-serif}
body{background:#07090d;color:#f8fafc;padding-bottom:84px}
/* M82 Institutional Cobalt Header */
.top{position:sticky;top:0;z-index:30;background:#001eff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px rgba(0,30,255,.35)}
.top-title{font-size:17px;font-weight:800;color:#fff;letter-spacing:.2px;display:flex;align-items:center;gap:8px}
.b{background:#111827;border:1px solid #ff5252;color:#ff5252;padding:4px 8px;border-radius:4px;font-size:10px;font-weight:800}
/* Sub-tabs (M82 Style) */
.subnav{display:flex;gap:6px;overflow-x:auto;background:#0b1120;padding:8px 12px;border-bottom:1px solid #1e293b}
.subnav button{background:#111827;border:1px solid #1f2937;color:#94a3b8;padding:5px 11px;border-radius:14px;font-size:11px;font-weight:700;white-space:nowrap}
.subnav button.act{background:#001eff;border-color:#3b82f6;color:#fff}
/* News Cards (Front Page + BUZZ badge) */
.card{padding:14px;border-bottom:1px solid #1e293b;cursor:pointer;background:#07090d}
.card:active{background:#111827}
.card h3{font-size:15px;line-height:1.38;margin:4px 0 8px;color:#f8fafc;font-weight:700}
.buzz{display:inline-block;background:#6d28d9;color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:4px;margin-right:6px;letter-spacing:.4px}
.tag{color:#60a5fa;font-size:10px;font-weight:700;border:1px solid #1d4ed8;background:#0f172a;padding:2px 6px;border-radius:4px;display:inline-block}
.meta-row{display:flex;align-items:center;gap:8px;margin-top:6px;font-size:11px;color:#94a3b8}
/* Market Cards */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:12px}
.box{background:#0d1117;border:1px solid #1f2937;border-radius:8px;padding:11px;transition:border-color .35s,background .35s;position:relative}
.box.up{border-color:#00e676;background:#062016}
.box.dn{border-color:#ff5252;background:#240b0e}
.star{position:absolute;top:8px;right:9px;font-size:14px;color:#475569;cursor:pointer}
.star.on{color:#fbbf24}
/* More Menu (M82 My Workspace Style) */
.ws-sec{padding:14px 14px 6px;font-size:13px;font-weight:800;color:#94a3b8;text-transform:uppercase;letter-spacing:.6px}
.ws-list{background:#0d1117;margin:0 12px 12px;border-radius:10px;border:1px solid #1f2937;overflow:hidden}
.ws-item{display:flex;justify-content:space-between;align-items:center;padding:14px;border-bottom:1px solid #1f2937;font-size:14px;font-weight:600;color:#f1f5f9;cursor:pointer}
.ws-item:last-child{border-bottom:none}
.ws-item:active{background:#1e293b}
.ws-val{font-size:12px;color:#38bdf8;font-family:monospace}
/* Search Input */
.srch-box{padding:12px;background:#0b1120;border-bottom:1px solid #1e293b}
.srch-inp{width:100%;background:#07090d;border:1px solid #3b82f6;color:#fff;padding:11px 14px;border-radius:8px;font-size:14px;outline:none}
/* Persistent Bottom Ticker & 5-Tab M82 Bar */
.tk{position:fixed;bottom:56px;left:0;right:0;z-index:25;background:#0b1120;border-top:1px solid #1e293b;padding:5px 10px;font-size:10px;font-family:monospace;display:flex;justify-content:space-between;color:#38bdf8;font-weight:700}
.nav{position:fixed;bottom:0;left:0;right:0;z-index:30;height:56px;background:#05070b;border-top:1px solid #1e293b;display:flex;justify-content:space-around;align-items:center}
.nav button{background:none;border:none;color:#64748b;font-size:10px;font-weight:700;padding:6px 4px;display:flex;flex-direction:column;align-items:center;gap:3px;flex:1}
.nav button.act{color:#3b82f6;border-top:2px solid #001eff}
.tab{display:none}.tab.act{display:block}
/* M82 Sign-In Overlay */
#login-scr{position:fixed;inset:0;z-index:100;background:#001eff;color:#fff;display:none;flex-direction:column;justify-content:space-between;padding:28px 20px}
.l-card{background:#fff;color:#0f172a;border-radius:10px;padding:18px;margin-top:20px}
.l-inp{width:100%;border:1px solid #cbd5e1;padding:11px;border-radius:6px;font-size:15px;font-weight:600;margin-top:6px;color:#0f172a}
.l-btn{width:100%;background:#001eff;color:#fff;border:none;padding:14px;border-radius:8px;font-size:15px;font-weight:800;margin-top:14px;cursor:pointer}

.casc-sec{padding:16px 14px 8px;font-size:12px;font-weight:800;color:#60a5fa;text-transform:uppercase;letter-spacing:.7px}
.casc-list{background:#0d1117;margin:0 12px 12px;border-radius:10px;border:1px solid #1f2937;overflow:hidden}
.casc-row{display:flex;justify-content:space-between;align-items:center;padding:15px 14px;border-bottom:1px solid #1f2937;font-size:14px;font-weight:700;color:#f8fafc;cursor:pointer}
.casc-row:last-child{border-bottom:none}
.casc-row:active{background:#1e293b}
.casc-row small{display:block;font-size:11px;font-weight:400;color:#94a3b8;margin-top:3px}
.pager-bar{display:flex;justify-content:space-between;align-items:center;background:#0b1120;padding:10px 12px;border-bottom:1px solid #1e293b;gap:6px}
.pg-btn{background:#111827;border:1px solid #1f2937;color:#e2e8f0;padding:6px 10px;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer}
.pg-btn.pri{background:#001eff;border-color:#3b82f6;color:#fff}
.pg-mid{font-size:12px;font-weight:800;color:#e2e8f0;text-align:center;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}

/* M82 v2.4.3 Android High-Legibility Executive Scale */
html, body { font-size: 16px !important; -webkit-text-size-adjust: 100%; }
.casc-sec { font-size: 13px !important; padding: 18px 16px 9px !important; }
.casc-row { font-size: 17px !important; padding: 18px 16px !important; line-height: 1.35 !important; }
.casc-row small { font-size: 13.5px !important; margin-top: 5px !important; line-height: 1.35 !important; }
.casc-row span { font-size: 22px !important; }
.pg-mid { font-size: 14px !important; }
.pg-btn { font-size: 13px !important; padding: 8px 12px !important; }
#nl div, .news-item, .card { font-size: 16px !important; line-height: 1.45 !important; }
#nl b, #nl strong, .n-title { font-size: 16.5px !important; line-height: 1.4 !important; }
#nl small, .n-meta, .ts { font-size: 13px !important; }
.nav button { font-size: 12.5px !important; }
#hdr-title { font-size: 18px !important; }
</style></head><body>

<!-- M82-Style Sovereign Sign In Screen -->
<div id="login-scr">
  <div>
    <div style="font-size:14px;font-weight:700;opacity:.9;margin-top:18px">Sign in with:</div>
    <div style="font-size:36px;font-weight:900;line-height:1.1;margin-top:6px">M82 Quantum<br>Workspace</div>
    <div class="l-card">
      <div style="font-size:11px;font-weight:800;color:#64748b">USER ID</div>
      <input id="uid-inp" class="l-inp" value="jmmp@molina82.com">
      <div style="font-size:11px;font-weight:800;color:#64748b;margin-top:12px">GATEWAY KEY</div>
      <input id="key-inp" type="password" class="l-inp" placeholder="Ingrese Token Soberano">
      <div id="l-err" style="color:#dc2626;font-size:12px;font-weight:700;margin-top:8px;display:none"></div>
      <button class="l-btn" onclick="doLogin()">SIGN IN WITH TOKEN</button>
      <button id="bio-btn" class="l-btn" style="background:#0f172a;margin-top:10px" onclick="doBioLogin()">&#128070; FINGERPRINT / QUICK PIN</button>
    </div>
  </div>
  <div style="font-size:11px;opacity:.85;text-align:center">Molina Holdings LLC &bull; Nodo Charallave L4/L5 Edge &bull; BUNKER 0.30x LOCK</div>
</div>

<div class="top">
  <div class="top-title" id="hdr-title">&#9776; Front Page</div>
  <span class="b">&#128274; BUNKER 0.30x</span>
</div>

<!-- 1. NEWS TAB: 3-Level M82 Taxonomy -->
<div id="t-n" class="tab act">
  <div id="news-lvl1"></div>
  <div id="news-lvl2" style="display:none">
    <div class="pager-bar"><button class="pg-btn" onclick="showLvl1()">&#8249; News</button><div class="pg-mid" id="lvl2-title">Category</div><div style="width:52px"></div></div>
    <div id="news-lvl2-list"></div>
  </div>
  <div id="news-lvl3" style="display:none">
    <div class="pager-bar"><button class="pg-btn" id="lvl3-back" onclick="backFromFeed()">&#8249; Atrás</button><button class="pg-btn" onclick="stepSubDesk(-1)">&#9664;</button><div class="pg-mid" id="pg-label">1 / 1 &mdash; Front Page</div><button class="pg-btn pri" onclick="stepSubDesk(1)">Sig &#8212; &#9654;</button></div>
    <div id="nl"></div>
  </div>
</div>

<!-- 2. MARKETS TAB -->
<div id="t-m" class="tab">
  <div class="subnav" id="mkt-filters">
    <button class="act" onclick="setMFilter('ALL',this)">All (26)</button>
    <button onclick="setMFilter('ENERGY',this)">Energy</button>
    <button onclick="setMFilter('INDICES',this)">Indices</button>
    <button onclick="setMFilter('RATES',this)">Rates &amp; FX</button>
    <button onclick="setMFilter('EQUITY',this)">Equities &amp; Crypto</button>
  </div>
  <div class="grid" id="mg"></div>
</div>

<!-- 3. WATCHLISTS & PORTFOLIO TAB -->
<div id="t-w" class="tab">
  <div class="grid">
    <div class="box"><small style="color:#94a3b8">EXPOSICION</small><h2>0.22x / 0.30x</h2></div>
    <div class="box"><small style="color:#94a3b8">DRY POWDER</small><h2 style="color:#00e676">78.0%</h2></div>
    <div class="box"><small style="color:#94a3b8">VAR DIARIO</small><h2 style="color:#fbbf24">1.68%</h2></div>
    <div class="box"><small style="color:#94a3b8">WARSH SPREAD</small><h2>102.0 bps</h2></div>
  </div>
  <div class="ws-sec">My Watchlist (Toca &#9733; en Markets para fijar)</div>
  <div class="grid" id="wl-grid"></div>
  <div class="ws-sec">Active Tail-Risk Alerts</div>
  <div style="padding:0 12px" id="al"></div>
</div>

<!-- 4. SEARCH TAB -->
<div id="t-s" class="tab">
  <div class="srch-box"><input id="q-inp" class="srch-inp" placeholder="Buscar RIC (CLc1, US10YT, NDX) o titular..." oninput="renderAll()"></div>
  <div class="grid" id="srch-mkt"></div>
  <div id="srch-news"></div>
</div>

<!-- 5. MORE TAB (My Workspace M82 Style) -->
<div id="t-more" class="tab">
  <div class="ws-sec">My Workspace</div>
  <div class="ws-list">
    <div class="ws-item" onclick="alert('Chairman Juan M. Molina\nSession: jmmp@molina82.com\nRole: Chairman & CEO - Molina Holdings LLC')"><span>&#128100; Profile</span><span class="ws-val">jmmp@molina82.com</span></div>
    <div class="ws-item" onclick="sw('w','Watchlists',document.getElementById('nav-w'))"><span>&#128276; Alerts (Tail-Risk)</span><span class="ws-val" id="cnt-alerts">LIVE</span></div>
    <div class="ws-item" onclick="sw('w','Watchlists',document.getElementById('nav-w'))"><span>&#128188; Briefcase &amp; Watchlist</span><span class="ws-val" id="cnt-wl">PINNED</span></div>
    <div class="ws-item" onclick="sw('n','Front Page',document.getElementById('nav-n'))"><span>&#128197; Economic Events &amp; Wire</span><span class="ws-val">24/7 WAL</span></div>
    <div class="ws-item" onclick="sw('w','Watchlists',document.getElementById('nav-w'))"><span>&#128202; Portfolios (Bunker Risk)</span><span class="ws-val">0.22x / 0.30x</span></div>
    <div class="ws-item" onclick="alert('Dispatch Channels Active:\n- Telegram Sovereign Bot\n- Ntfy Priority Channel\n- M82 M82 Telemetry Bridge (2s WAL)')"><span>&#128172; Messenger &amp; Dispatch</span><span class="ws-val">ONLINE</span></div>
  </div>
  <div class="ws-sec">My App &amp; Governance</div>
  <div class="ws-list">
    <div class="ws-item"><span>Version</span><span class="ws-val">M82-M82 v2.0.0</span></div>
    <div class="ws-item"><span>Execution Node</span><span class="ws-val">Charallave L4/L5</span></div>
    <div class="ws-item"><span>Database Engine</span><span class="ws-val">SQLite WAL (?mode=ro)</span></div>
  </div>
  <div class="ws-sec">Session Control</div>
  <div class="ws-list">
    <div class="ws-item" style="color:#ff5252" onclick="doLogout()"><span>&#10140; Sign Out / Lock Terminal</span><span class="ws-val" style="color:#ff5252">LOCK</span></div>
  </div>
</div>

<div class="tk" id="tk"><span>WS: jmmp@molina82.com</span><span>WAL SYNC...</span></div>

<div class="nav">
  <button id="nav-n" class="act" onclick="sw('n','Front Page',this)"><span>&#128240;</span><span>News</span></button>
  <button id="nav-m" onclick="sw('m','Markets',this)"><span>&#128200;</span><span>Markets</span></button>
  <button id="nav-w" onclick="sw('w','Watchlists',this)"><span>&#128065;</span><span>Watchlists</span></button>
  <button id="nav-s" onclick="sw('s','Search',this)"><span>&#128269;</span><span>Search</span></button>
  <button id="nav-more" onclick="sw('more','More',this)"><span>&bull;&bull;&bull;</span><span>More</span></button>
</div>

<script>
const TOK = "__TOK__";
let prevQ = {}, dirQ = {}, lastData = {q:{}, m:[], a:[]};
let nFilter = 'ALL', mFilter = 'ALL';
let favs = new Set(JSON.parse(localStorage.getItem('m82_favs') || '["CLc1","LCOc1","US10YT=RR","GC=F","BTC-USD","NDX"]'));

if(localStorage.getItem('m82_locked') === '1'){
  document.getElementById('login-scr').style.display = 'flex';
}
function showErr(m){
  const e = document.getElementById('l-err');
  e.innerText = m; e.style.display = 'block';
}
async function enrollBio(){
  if(!window.PublicKeyCredential) return;
  try{
    const ch = new Uint8Array(32); crypto.getRandomValues(ch);
    const uid = new TextEncoder().encode("jmmp@molina82.com");
    const cred = await navigator.credentials.create({publicKey:{
      challenge: ch,
      rp: {name: "M82 Sovereign Terminal"},
      user: {id: uid, name: "jmmp@molina82.com", displayName: "Chairman Juan M. Molina"},
      pubKeyCredParams: [{type:"public-key", alg:-7}, {type:"public-key", alg:-257}],
      authenticatorSelection: {authenticatorAttachment:"platform", userVerification:"required"},
      timeout: 60000
    }});
    if(cred){
      const raw = btoa(String.fromCharCode(...new Uint8Array(cred.rawId)));
      localStorage.setItem('m82_bio_id', raw);
      return;
    }
  }catch(e){}
  const pin = prompt("WebView sin sensor directo. Cree un PIN Soberano de 4 dígitos para acceso rápido:");
  if(pin && pin.trim().length >= 4) localStorage.setItem('m82_quick_pin', pin.trim());
}
async function doLogin(){
  const k = document.getElementById('key-inp').value.trim();
  if(k !== TOK){ showErr("ACCESO DENEGADO: GATEWAY KEY INVÁLIDO"); return; }
  document.getElementById('l-err').style.display = 'none';
  if(!localStorage.getItem('m82_bio_id')) await enrollBio();
  localStorage.setItem('m82_locked', '0');
  document.getElementById('login-scr').style.display = 'none';
}
async function doBioLogin(){
  const saved = localStorage.getItem('m82_bio_id');
  const qpin = localStorage.getItem('m82_quick_pin');
  if(!saved && qpin){
    const inp = prompt("Ingrese su PIN Soberano:");
    if(inp && inp.trim() === qpin){
      document.getElementById('l-err').style.display = 'none';
      localStorage.setItem('m82_locked', '0');
      document.getElementById('login-scr').style.display = 'none';
    } else if(inp !== null) { showErr("PIN Soberano incorrecto."); }
    return;
  }
  if(!saved){ showErr("Ingrese su Gateway Key una vez para vincular huella o PIN."); return; }
  if(!window.PublicKeyCredential){ showErr("Sensor no expuesto en WebView. Reingrese Gateway Key para fijar PIN."); return; }
  try{
    const ch = new Uint8Array(32); crypto.getRandomValues(ch);
    const rawId = Uint8Array.from(atob(saved), c => c.charCodeAt(0));
    const assertion = await navigator.credentials.get({publicKey:{
      challenge: ch,
      allowCredentials: [{type:"public-key", id: rawId}],
      userVerification: "required",
      timeout: 60000
    }});
    if(assertion){
      document.getElementById('l-err').style.display = 'none';
      localStorage.setItem('m82_locked', '0');
      document.getElementById('login-scr').style.display = 'none';
    }
  }catch(e){ showErr("Verificación biométrica cancelada o fallida."); }
}
function doLogout(){
  localStorage.setItem('m82_locked', '1');
  document.getElementById('login-scr').style.display = 'flex';
}

const M82_TAXONOMY=[
{group:"M82 Sovereign Wire",direct:true,items:[{label:"Front Page",sub:"Despacho ejecutivo global en vivo",rx:""},{label:"Central Banks & Global Economy",sub:"Fed, tasas, inflación y liquidez macro",rx:"FED|RATE|GDP|INFLATION|CPI|BOJ|CENTRAL|ECONOMY"},{label:"Sustainable Finance",sub:"Transición energética, ESG y flujos verdes",rx:"GREEN|SOLAR|CLIMATE|ESG|TRANSITION|CARBON"},{label:"Regulation & Compliance",sub:"Política monetaria, sanciones y regulación",rx:"REGULAT|SEC|SANCTION|COMPLIANCE|POLICY|TARIFF"}]},
{group:"News Categories",direct:false,categories:[
{name:"Banking & Finance",sub:"Financial Services, Investment Banking, Crypto",subs:[{label:"Financial Services",rx:"BANK|FINANCIAL|CREDIT|INSURANCE|FINTECH"},{label:"Investment Banking",rx:"M&A|IPO|DEAL|GOLDMAN|JPM|MORGAN|CAPITAL"},{label:"Fixed Income & Rates",rx:"BOND|TREASURY|YIELD|10Y|2Y|SPREAD|DEBT"},{label:"Digital Finance & Crypto",rx:"BTC|BITCOIN|CRYPTO|ETH|BLOCKCHAIN|DIGITAL"}]},
{name:"Commentary",sub:"M82 Breakingviews, Open Interest, FX Comment",subs:[{label:"M82 Breakingviews",rx:"ANALYSIS|OUTLOOK|VIEW|STRATEGY|RISK"},{label:"M82 Open Interest",rx:"FUTURES|POSITION|HEDGE|FUND|FLOW"},{label:"FX & Macro Desk Comment",rx:"USD|JPY|EUR|DXY|FX|CURRENCY|DOLLAR"}]},
{name:"Companies",sub:"U.S., European & Asian Corporates",subs:[{label:"U.S. Companies",rx:"US|NVDA|AAPL|MSFT|TECH|AI|EARNINGS|WALL STREET"},{label:"European Companies",rx:"EUROPE|DAX|FTSE|STOXX|EU|GERMAN|UK"},{label:"Asian Companies",rx:"ASIA|CHINA|JAPAN|NIKKEI|KOREA|TAIWAN|TSMC"}]},
{name:"Commodities",sub:"Energy, Metals, Agriculture, Gas & LNG",subs:[{label:"Commodities Overview",rx:"COMMODIT|RAW|SUPPLY|OPEC"},{label:"Energy (WTI / Brent / Crack)",rx:"OIL|WTI|BRENT|CRUDE|CRACK|REFIN|OPEC"},{label:"Metals (Gold / Silver / Copper)",rx:"GOLD|SILVER|COPPER|METAL|MINING"},{label:"Agricultural Commodities",rx:"WHEAT|CORN|SOY|GRAIN|AGRI|COFFEE"},{label:"Global Gas, Power & LNG",rx:"GAS|LNG|POWER|ELECTRIC|NATGAS"}]},
{name:"Industries",sub:"TMT, Heavy Industry, Consumer & Healthcare",subs:[{label:"Technology, Media & Telecoms",rx:"AI|TECH|CHIP|SEMICONDUCTOR|CLOUD|TELECOM"},{label:"Heavy Industry & Transport",rx:"INDUSTR|TRANSPORT|AVIATION|FLIGHT|SHIPPING|AUTO"},{label:"Consumer & Retail",rx:"CONSUMER|RETAIL|SPENDING|HOUSEHOLD"},{label:"Healthcare & Pharma",rx:"HEALTH|PHARMA|BIOTECH|DRUG|MEDICAL"}]},
{name:"Regional",sub:"Latin America, U.S., Europe, Middle East, Asia",subs:[{label:"Latin America",rx:"LATAM|VENEZUELA|BRAZIL|MEXICO|ARGENTINA|CHILE"},{label:"United States",rx:"US|U\.S\.|FED|WASHINGTON|AMERICAN"},{label:"Canada",rx:"CANADA|TORONTO|BOC|CAD"},{label:"Europe & Russia",rx:"EUROPE|RUSSIA|UKRAINE|ECB|EUROZONE|GERMANY"},{label:"United Kingdom",rx:"UK|BRITAIN|BOE|LONDON|STERLING"},{label:"Middle East & Africa",rx:"MIDDLE EAST|SAUDI|IRAN|ISRAEL|AFRICA|GULF"},{label:"Greater China",rx:"CHINA|BEIJING|HONG KONG|YUAN|PBOC"},{label:"Japan & the Koreas",rx:"JAPAN|BOJ|YEN|KOREA|TOKYO|SEOUL"},{label:"Southeast Asia",rx:"ASEAN|SINGAPORE|INDONESIA|VIETNAM|THAILAND"},{label:"India & South Asia",rx:"INDIA|MUMBAI|RBI|RUPEE"},{label:"Australia & New Zealand",rx:"AUSTRALIA|RBA|SYDNEY|NEW ZEALAND"}]},
{name:"National Languages",sub:"Español, English, Português, Deutsch, Français, 日本語",subs:[{label:"Español (M82 Wire)",rx:""},{label:"Global English Desk",rx:""},{label:"Brasil / Português",rx:"BRAZIL|BRASIL|REAL|BCB"},{label:"Deutschland / Deutsch",rx:"GERMAN|DAX|BUND|BERLIN"},{label:"France / Français",rx:"FRANCE|PARIS|CAC|ECB"},{label:"Japan / 日本語デスク",rx:"JAPAN|BOJ|NIKKEI|YEN"}]},
{name:"Sports & Lifestyle",sub:"Sports, Executive Lifestyle & Global Events",subs:[{label:"Sports",rx:"SPORT|OLYMPIC|FIFA|F1|CHAMPION"},{label:"Lifestyle & Entertainment",rx:"LIFESTYLE|TRAVEL|LUXURY|CULTURE"}]}
]}];
let activeSubList=M82_TAXONOMY[0].items,curSubIdx=0,activeRx="",cameFromLvl2=false;

function checkDeepLink(){
  const u = new URLSearchParams(window.location.search);
  const q = u.get("q") || "";
  const desk = u.get("desk") || "";
  if(!q && !desk) return;
  activeRx = q ? q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") : desk;
  cameFromLvl2 = false;
  document.getElementById("news-lvl1").style.display = "none";
  document.getElementById("news-lvl2").style.display = "none";
  document.getElementById("news-lvl3").style.display = "block";
  document.getElementById("hdr-title").innerText = desk || "M82 Breaking Alert";
  document.getElementById("lvl3-back").innerHTML = "&#8249; News";
  document.getElementById("pg-label").innerHTML = "ALERTA EN VIVO &mdash; " + (desk || "M82 Wire");
}

function buildLvl1(){let h="";M82_TAXONOMY.forEach(sec=>{h+=`<div class="casc-sec">${sec.group}</div><div class="casc-list">`;if(sec.direct){sec.items.forEach((it,idx)=>{h+=`<div class="casc-row" onclick="openDirectFeed(${idx})"><div>${it.label}<small>${it.sub}</small></div><span>&#8250;</span></div>`;});}else{sec.categories.forEach((cat,cIdx)=>{h+=`<div class="casc-row" onclick="openLvl2(${cIdx})"><div>${cat.name}<small>${cat.sub}</small></div><span>&#8250;</span></div>`;});}h+=`</div>`;});document.getElementById("news-lvl1").innerHTML=h;}
function showLvl1(){document.getElementById("news-lvl1").style.display="block";document.getElementById("news-lvl2").style.display="none";document.getElementById("news-lvl3").style.display="none";document.getElementById("hdr-title").innerHTML="&#9776; News";}
function openLvl2(cIdx){const cat=M82_TAXONOMY[1].categories[cIdx];activeSubList=cat.subs;cameFromLvl2=true;document.getElementById("news-lvl1").style.display="none";document.getElementById("news-lvl3").style.display="none";document.getElementById("news-lvl2").style.display="block";document.getElementById("hdr-title").innerText=cat.name;document.getElementById("lvl2-title").innerText=cat.name;let h=`<div class="casc-list" style="margin-top:12px">`;cat.subs.forEach((sb,idx)=>{h+=`<div class="casc-row" onclick="openLvl3(${idx},true)"><div>${sb.label}</div><span>&#8250;</span></div>`;});h+=`</div>`;document.getElementById("news-lvl2-list").innerHTML=h;}
function openDirectFeed(idx){activeSubList=M82_TAXONOMY[0].items;cameFromLvl2=false;openLvl3(idx,false);}
function openLvl3(idx,from2){curSubIdx=(idx+activeSubList.length)%activeSubList.length;const item=activeSubList[curSubIdx];activeRx=item.rx||"";document.getElementById("news-lvl1").style.display="none";document.getElementById("news-lvl2").style.display="none";document.getElementById("news-lvl3").style.display="block";document.getElementById("hdr-title").innerText=item.label;document.getElementById("lvl3-back").innerHTML=from2?"&#8249; Sub-Desks":"&#8249; News";document.getElementById("pg-label").innerHTML=`${curSubIdx+1}/${activeSubList.length} &mdash; ${item.label}`;renderAll();}
function stepSubDesk(d){openLvl3(curSubIdx+d,cameFromLvl2);}
function backFromFeed(){if(cameFromLvl2){document.getElementById("news-lvl3").style.display="none";document.getElementById("news-lvl2").style.display="block";}else{showLvl1();}}
function sw(t,title,b){document.querySelectorAll(".tab").forEach(e=>e.classList.remove("act"));document.getElementById("t-"+t).classList.add("act");document.querySelectorAll(".nav button").forEach(e=>e.classList.remove("act"));if(b)b.classList.add("act");if(t==="n"){showLvl1();}else{document.getElementById("hdr-title").innerText=title;}}
function setNFilter(f,b){}
function setMFilter(f, b){
  mFilter = f;
  document.querySelectorAll('#mkt-filters button').forEach(x=>x.classList.remove('act'));
  b.classList.add('act');
  renderAll();
}
function toggleFav(e, k){
  e.stopPropagation();
  if(favs.has(k)) favs.delete(k); else favs.add(k);
  localStorage.setItem('m82_favs', JSON.stringify([...favs]));
  renderAll();
}

function fmtInst(k, v){
  if(typeof v !== 'number') return String(v);
  const pct = new Set(['US10YT=RR','US2YT=RR','US30YT=RR','VIX','OVX','GVZ']);
  const idx = new Set(['DXY','.DXY','DX-Y.NYB','NQ=F','NDX','ES=F','YM=F','RTY=F','N225','^N225','GDAXI','^GDAXI','ZB=F']);
  const s = v.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
  if(pct.has(k) || k.includes('YT=') || k.endsWith('_pct')) return s + '%';
  if(idx.has(k)) return s;
  return '$' + s;
}

function catOf(k){
  if(/CL|LCO|BZ|RB|HO|crack|brent/i.test(k)) return 'ENERGY';
  if(/NQ|NDX|ES|YM|RTY|GDAXI|N225|ZB/i.test(k)) return 'INDICES';
  if(/YT=|DXY|DX-Y/i.test(k)) return 'RATES';
  return 'EQUITY';
}

function renderCardBox(k, v){
  const st = dirQ[k] || '';
  const vCol = st==='up' ? '#00e676' : (st==='dn' ? '#ff5252' : '#f8fafc');
  const arr = st==='up' ? ' &#9650;' : (st==='dn' ? ' &#9660;' : '');
  const on = favs.has(k) ? 'on' : '';
  return `<div class="box ${st}"><span class="star ${on}" onclick="toggleFav(event,'${k}')">&#9733;</span><small style="color:#94a3b8">${k}</small><h2 style="color:${vCol};font-size:17px;margin-top:3px">${fmtInst(k,v)}${arr}</h2></div>`;
}

function renderNewsCard(x){
  const rVal = parseFloat(x.r || 0);
  const buzz = rVal >= 4.0 ? `<span class="buzz">BUZZ</span>` : '';
  return `<div class="card" data-id="${x.id||'latest'}"><h3>${x.h}</h3><div>${buzz}<span class="tag">${x.t || 'M82_QUANTUM_WIRE'}</span> <small style="color:#fbbf24;margin-left:6px">RISK ${x.r}</small></div><div class="meta-row"><span>${x.s}</span><span>&bull;</span><span>${(x.ts||'').slice(0,16)}</span></div></div>`;
}

function renderAll(){
  const q = lastData.q || {};
  const skip = new Set(['source','captured_at','user','status','ts','workspace']);
  const entries = Object.entries(q).filter(([k,v])=>!skip.has(k) && v!==null && typeof v!=='object');

  // News filtered by 3-Level Taxonomy
  let newsFiltered = (lastData.m || []);
  if(activeRx){const rxObj=new RegExp(activeRx,"i");const m=newsFiltered.filter(x=>rxObj.test((x.h||"")+" "+(x.c||"")+" "+(x.t||"")));if(m.length>0)newsFiltered=m;}
  document.getElementById('nl').innerHTML = newsFiltered.map(renderNewsCard).join('') || '<div style="padding:20px;color:#64748b">Sin despachos en este filtro.</div>';

  // Markets filtered
  const mktFiltered = entries.filter(([k])=> mFilter==='ALL' || catOf(k)===mFilter);
  document.getElementById('mg').innerHTML = `<div class="box" style="grid-column:span 2;border-color:#001eff;background:#0b1536"><small style="color:#60a5fa">M82 QUANTUM DESK &bull; jmmp@molina82.com</small><h2 style="font-size:14px;margin-top:3px">${mktFiltered.length} INSTRUMENTOS EN VIVO (TICK 2s WAL)</h2></div>` + mktFiltered.map(([k,v])=>renderCardBox(k,v)).join('');

  // Watchlist pinned
  const pinned = entries.filter(([k])=>favs.has(k));
  document.getElementById('wl-grid').innerHTML = pinned.map(([k,v])=>renderCardBox(k,v)).join('');
  document.getElementById('cnt-wl').innerText = pinned.length + ' RICS';
  document.getElementById('cnt-alerts').innerText = (lastData.a||[]).length + ' ACTIVE';

  // Alerts
  document.getElementById('al').innerHTML = (lastData.a||[]).map(a=>`<div class="card" data-id="A-${a.id||1}" style="border-radius:8px;margin-bottom:8px;border:1px solid #1f2937"><span class="buzz" style="background:#b91c1c">${a.t}</span><h3 style="margin-top:6px;font-size:13px">${a.h}</h3><small style="color:#fbbf24">TAIL-RISK SCORE: ${a.r}</small></div>`).join('');

  // Search
  const term = (document.getElementById('q-inp').value || '').trim().toUpperCase();
  if(term){
    const sm = entries.filter(([k])=>k.toUpperCase().includes(term));
    const sn = (lastData.m||[]).filter(x=>(x.h+' '+x.s+' '+x.t).toUpperCase().includes(term));
    document.getElementById('srch-mkt').innerHTML = sm.map(([k,v])=>renderCardBox(k,v)).join('');
    document.getElementById('srch-news').innerHTML = sn.map(renderNewsCard).join('');
  } else {
    document.getElementById('srch-mkt').innerHTML = '';
    document.getElementById('srch-news').innerHTML = '<div style="padding:20px;color:#64748b;font-size:13px">Escriba un RIC (ej. LCOc1, US10YT, GC=F) o palabra clave para buscar en tiempo real.</div>';
  }
}

async function ld(){
  try{
    const r = await fetch('/api?token='+TOK, {headers:{'X-M82-Token':TOK}});
    const d = await r.json();
    const q = d.q || {};
    Object.entries(q).forEach(([k,v])=>{
      if(typeof v==='number' && typeof prevQ[k]==='number'){
        if(v > prevQ[k]) dirQ[k] = 'up';
        else if(v < prevQ[k]) dirQ[k] = 'dn';
      }
      if(typeof v==='number') prevQ[k] = v;
    });
    lastData = d;
    document.getElementById('tk').innerHTML = `<span>WTI ${fmtInst('CLc1',q.CLc1||99.5)}</span><span>BRENT ${fmtInst('LCOc1',q.LCOc1||114.72)}</span><span>CRACK ${fmtInst('crack_321_usd',q.crack_321_usd||37.42)}</span><span>10Y ${fmtInst('US10YT=RR',q['US10YT=RR']||4.38)}</span>`;
    renderAll();
  }catch(e){}
}

buildLvl1();
checkDeepLink();
ld();
setInterval(ld, 2000);

document.addEventListener('click', e=>{
  const card = e.target.closest('.card');
  if(card && !e.target.closest('a,button,.star')){
    const idAttr = card.getAttribute('data-id') || 'latest';
    window.location.href = '/dispatch/' + encodeURIComponent(idAttr);
  }
});
</script></body></html>""".replace("__TOK__", TOK)

class M82MobileRequestHandler(BaseHTTPRequestHandler):
    def _safe_write(self, b):
        try: self.wfile.write(b)
        except (BrokenPipeError, ConnectionResetError): pass
    def do_GET(self):
        p_clean = self.path.split("?")[0]
        if p_clean in ("/icon.png", "/icon-192.png", "/icon-512.png"):
            fn = "icon-512.png" if "512" in p_clean else "icon-192.png"
            data = open(os.path.join(ROOT, "orchestrator", fn), "rb").read()
            self.send_response(200); self.send_header("Content-Type", "image/png"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        if p_clean == "/manifest.json":
            mf = b'{"name":"M82 Quantum Wire","short_name":"M82 Wire","start_url":"/","display":"standalone","background_color":"#07090d","theme_color":"#001eff","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png"}]}'
            self.send_response(200); self.send_header("Content-Type", "application/manifest+json"); self.send_header("Content-Length", str(len(mf))); self.end_headers(); self.wfile.write(mf); return
        if p_clean.startswith("/dispatch/"):
            did = unquote(p_clean.replace("/dispatch/", "", 1)) or "latest"
            body = render_dispatch(did).encode()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self._safe_write(body); return
        if p_clean.startswith("/api"):
            if self.headers.get("X-M82-Token") != TOK and f"token={TOK}" not in self.path:
                self.send_response(401); self.end_headers(); self.wfile.write(b"UNAUTHORIZED"); return
            payload = json.dumps(state()).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(payload))); self.end_headers(); self.wfile.write(payload); return
        body = HTML.encode()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self._safe_write(body)
    def log_message(self, *a): pass

HTTPServer.allow_reuse_address = True
ThreadingHTTPServer(("0.0.0.0", 8282), M82MobileRequestHandler).serve_forever()
