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
            rows = c2.execute("SELECT id, source, category, headline, risk_score, m82_tag, created_at FROM macro_dossier WHERE headline NOT LIKE '%Live Poll 20 activos%' AND headline NOT LIKE '%Multichannel Telegram%' ORDER BY id DESC LIMIT 35").fetchall()
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
                cat, title, risk, source, tag = str(row[0]), str(row[1]), str(row[2]), "M82 TAIL-RISK ENGINE", "TAIL_RISK_ALERT"
                body = title
        else:
            q_sql = f"SELECT source, category, headline, risk_score, m82_tag, created_at, {extra_col} FROM macro_dossier " + ("ORDER BY id DESC LIMIT 1" if item_id == "latest" else "WHERE id=?")
            row = c2.execute(q_sql).fetchone() if item_id == "latest" else c2.execute(q_sql, (item_id,)).fetchone()
            if row:
                source, cat, title, risk, tag, ts, body = [str(x or "") for x in row]
        c2.close()
    except Exception as e:
        body = f"Lectura RAM WAL: {e}"
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{background:#07090d;color:#e8f0fe;font-family:sans-serif;margin:0;padding:16px}}.bar{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1e293b;padding-bottom:12px;margin-bottom:16px}}.btn{{background:#001eff;color:#fff;border:none;padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:700;font-size:12px}}.bunker{{background:#2a080d;border:1px solid #ff1744;color:#ff5252;padding:6px 10px;border-radius:4px;font-size:11px;font-weight:700}}.card{{background:#0d1117;border:1px solid #1f2937;border-radius:8px;padding:16px}}.meta{{color:#94a3b8;font-size:12px;margin-bottom:8px;font-family:monospace}}h1{{font-size:18px;line-height:1.4;margin:8px 0 14px;color:#fff}}.body{{font-size:14px;line-height:1.65;color:#cbd5e1;white-space:pre-wrap;border-top:1px solid #1f2937;padding-top:12px}}.tag{{display:inline-block;background:#1e1b4b;color:#a5b4fc;border:1px solid #4338ca;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:700;margin-right:6px}}/* Category Drawer (100% M82 Proprietary Brand) */
#cat-drawer{position:fixed;inset:0;z-index:80;background:#07090d;display:none;flex-direction:column;overflow-y:auto;padding-bottom:30px}
.cd-top{background:#001eff;padding:14px 16px;display:flex;justify-content:space-between;align-items:center}
.cd-sec{padding:16px 16px 8px;font-size:13px;font-weight:800;color:#94a3b8;text-transform:uppercase;letter-spacing:.6px}
.cd-item{padding:15px 16px;border-bottom:1px solid #1e293b;font-size:15px;font-weight:600;color:#f8fafc;display:flex;justify-content:space-between;align-items:center;cursor:pointer}
.cd-item.sel{border-left:4px solid #3b82f6;background:#0f172a}
.cd-item:active{background:#1e293b}
</style></head><body><div class="bar"><a class="btn" href="/">&#8592; Front Page</a><span class="bunker">&#128274; BUNKER 0.30x LOCK</span></div><div class="card"><div class="meta">ID #{html.escape(str(item_id))} &bull; {html.escape(source)} &bull; {html.escape(ts)}</div><div><span class="tag">{html.escape(cat)}</span><span class="tag" style="color:#fbbf24;border-color:#b45309;background:#451a03">RISK {html.escape(risk)}</span><span class="tag">{html.escape(tag)}</span></div><h1>{html.escape(title)}</h1><div class="body">{html.escape(body or title)}</div></div></body></html>"""

HTML = """<!doctype html><html><head><meta charset="utf-8"><link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#001eff"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,sans-serif}
body{background:#07090d;color:#f8fafc;padding-bottom:84px}
/* LSEG Institutional Cobalt Header */
.top{position:sticky;top:0;z-index:30;background:#001eff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 10px rgba(0,30,255,.35)}
.top-title{font-size:17px;font-weight:800;color:#fff;letter-spacing:.2px;display:flex;align-items:center;gap:8px}
.b{background:#111827;border:1px solid #ff5252;color:#ff5252;padding:4px 8px;border-radius:4px;font-size:10px;font-weight:800}
/* Sub-tabs (LSEG Style) */
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
/* More Menu (LSEG My Workspace Style) */
.ws-sec{padding:14px 14px 6px;font-size:13px;font-weight:800;color:#94a3b8;text-transform:uppercase;letter-spacing:.6px}
.ws-list{background:#0d1117;margin:0 12px 12px;border-radius:10px;border:1px solid #1f2937;overflow:hidden}
.ws-item{display:flex;justify-content:space-between;align-items:center;padding:14px;border-bottom:1px solid #1f2937;font-size:14px;font-weight:600;color:#f1f5f9;cursor:pointer}
.ws-item:last-child{border-bottom:none}
.ws-item:active{background:#1e293b}
.ws-val{font-size:12px;color:#38bdf8;font-family:monospace}
/* Search Input */
.srch-box{padding:12px;background:#0b1120;border-bottom:1px solid #1e293b}
.srch-inp{width:100%;background:#07090d;border:1px solid #3b82f6;color:#fff;padding:11px 14px;border-radius:8px;font-size:14px;outline:none}
/* Persistent Bottom Ticker & 5-Tab LSEG Bar */
.tk{position:fixed;bottom:56px;left:0;right:0;z-index:25;background:#0b1120;border-top:1px solid #1e293b;padding:5px 10px;font-size:10px;font-family:monospace;display:flex;justify-content:space-between;color:#38bdf8;font-weight:700}
.nav{position:fixed;bottom:0;left:0;right:0;z-index:30;height:56px;background:#05070b;border-top:1px solid #1e293b;display:flex;justify-content:space-around;align-items:center}
.nav button{background:none;border:none;color:#64748b;font-size:10px;font-weight:700;padding:6px 4px;display:flex;flex-direction:column;align-items:center;gap:3px;flex:1}
.nav button.act{color:#3b82f6;border-top:2px solid #001eff}
.tab{display:none}.tab.act{display:block}
/* LSEG Sign-In Overlay */
#login-scr{position:fixed;inset:0;z-index:100;background:#001eff;color:#fff;display:none;flex-direction:column;justify-content:space-between;padding:28px 20px}
.l-card{background:#fff;color:#0f172a;border-radius:10px;padding:18px;margin-top:20px}
.l-inp{width:100%;border:1px solid #cbd5e1;padding:11px;border-radius:6px;font-size:15px;font-weight:600;margin-top:6px;color:#0f172a}
.l-btn{width:100%;background:#001eff;color:#fff;border:none;padding:14px;border-radius:8px;font-size:15px;font-weight:800;margin-top:14px;cursor:pointer}
</style></head><body>

<!-- LSEG-Style Sovereign Sign In Screen -->
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

<!-- M82 Sovereign News Categories Drawer -->
<div id="cat-drawer">
  <div class="cd-top">
    <span style="font-size:20px;font-weight:800;color:#fff">News Categories</span>
    <span style="font-size:22px;color:#fff;cursor:pointer;padding:0 6px" onclick="toggleDrawer(false)">&#10005;</span>
  </div>
  <div class="cd-sec">M82 Sovereign Wire</div>
  <div class="cd-item sel" onclick="pickCat('ALL','Front Page')"><span>Front Page</span><span>&#8250;</span></div>
  <div class="cd-item" onclick="pickCat('MACRO','Central Banks & Global Economy')"><span>Central Banks &amp; Global Economy</span><span>&#8250;</span></div>
  <div class="cd-item" onclick="pickCat('ENERGY','Commodities & Energy')"><span>Commodities &amp; Energy</span><span>&#8250;</span></div>
  <div class="cd-item" onclick="pickCat('RISK','Regulation & Tail-Risk')"><span>Regulation &amp; Tail-Risk</span><span>&#8250;</span></div>
  <div class="cd-sec">Desk Coverage</div>
  <div class="cd-item" onclick="pickCat('BANKING','Banking & Finance')"><span>Banking &amp; Finance</span><span>&#8250;</span></div>
  <div class="cd-item" onclick="pickCat('COMPANIES','Companies & Equities')"><span>Companies &amp; Equities</span><span>&#8250;</span></div>
  <div class="cd-item" onclick="pickCat('MARKETS','Markets & Rates')"><span>Markets &amp; Rates</span><span>&#8250;</span></div>
  <div class="cd-item" onclick="pickCat('REGIONAL','Regional & LatAm')"><span>Regional &amp; LatAm</span><span>&#8250;</span></div>
</div>
<div class="top">
  <div class="top-title" id="hdr-title" onclick="if(document.getElementById('t-n').classList.contains('act'))toggleDrawer(true)" style="cursor:pointer">&#9776; Front Page</div>
  <span class="b">&#128274; BUNKER 0.30x</span>
</div>

<!-- 1. NEWS TAB (Front Page) -->
<div id="t-n" class="tab act">
  <div class="subnav" id="news-filters">
    <button class="act" onclick="setNFilter('ALL',this)">All Wire</button>
    <button onclick="setNFilter('ENERGY',this)">Energy &amp; Oil</button>
    <button onclick="setNFilter('MACRO',this)">Macro &amp; Rates</button>
    <button onclick="setNFilter('RISK',this)">High Risk (&ge;5)</button>
  </div>
  <div id="nl"></div>
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

<!-- 5. MORE TAB (My Workspace LSEG Style) -->
<div id="t-more" class="tab">
  <div class="ws-sec">My Workspace</div>
  <div class="ws-list">
    <div class="ws-item" onclick="alert('Chairman Juan M. Molina\nSession: jmmp@molina82.com\nRole: Chairman & CEO - Molina Holdings LLC')"><span>&#128100; Profile</span><span class="ws-val">jmmp@molina82.com</span></div>
    <div class="ws-item" onclick="sw('w','Watchlists',document.getElementById('nav-w'))"><span>&#128276; Alerts (Tail-Risk)</span><span class="ws-val" id="cnt-alerts">LIVE</span></div>
    <div class="ws-item" onclick="sw('w','Watchlists',document.getElementById('nav-w'))"><span>&#128188; Briefcase &amp; Watchlist</span><span class="ws-val" id="cnt-wl">PINNED</span></div>
    <div class="ws-item" onclick="sw('n','Front Page',document.getElementById('nav-n'))"><span>&#128197; Economic Events &amp; Wire</span><span class="ws-val">24/7 WAL</span></div>
    <div class="ws-item" onclick="sw('w','Watchlists',document.getElementById('nav-w'))"><span>&#128202; Portfolios (Bunker Risk)</span><span class="ws-val">0.22x / 0.30x</span></div>
    <div class="ws-item" onclick="alert('Dispatch Channels Active:\n- Telegram Sovereign Bot\n- Ntfy Priority Channel\n- M82 Real-Time Telemetry Bridge (2s WAL)')"><span>&#128172; Messenger &amp; Dispatch</span><span class="ws-val">ONLINE</span></div>
  </div>
  <div class="ws-sec">My App &amp; Governance</div>
  <div class="ws-list">
    <div class="ws-item"><span>Version</span><span class="ws-val">M82-QUANTUM v2.2.0</span></div>
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

function sw(t, title, b){
  document.querySelectorAll('.tab').forEach(e=>e.classList.remove('act'));
  document.getElementById('t-'+t).classList.add('act');
  document.querySelectorAll('.nav button').forEach(e=>e.classList.remove('act'));
  if(b) b.classList.add('act');
  document.getElementById('hdr-title').innerHTML = (t==='n' ? '&#9776; ' : '') + title;
}
function setNFilter(f, b){
  nFilter = f;
  document.querySelectorAll('#news-filters button').forEach(x=>x.classList.remove('act'));
  b.classList.add('act');
  renderAll();
}
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

function cleanBrand(str){
  return String(str || 'M82 Sovereign Wire').replace(/LSEG|Refinitiv|Reuters|WSJ/gi, 'M82 Wire');
}
function toggleDrawer(show){
  document.getElementById('cat-drawer').style.display = show ? 'flex' : 'none';
}
function pickCat(code, label){
  nFilter = code;
  toggleDrawer(false);
  document.getElementById('hdr-title').innerHTML = '&#9776; ' + label;
  renderAll();
}
function renderNewsCard(x){
  const rVal = parseFloat(x.r || 0);
  const buzz = rVal >= 4.0 ? `<span class="buzz">BUZZ</span>` : '';
  const tagClean = cleanBrand(x.t || 'M82_QUANTUM_WIRE');
  const srcClean = cleanBrand(x.s || 'M82 Sovereign Desk');
  return `<div class="card" data-id="${x.id||'latest'}"><h3>${x.h}</h3><div>${buzz}<span class="tag">${tagClean}</span> <small style="color:#fbbf24;margin-left:6px">RISK ${x.r}</small></div><div class="meta-row"><span>${srcClean}</span><span>&bull;</span><span>${(x.ts||'').slice(0,16)}</span></div></div>`;
}

function renderAll(){
  const q = lastData.q || {};
  const skip = new Set(['source','captured_at','user','status','ts','workspace']);
  const entries = Object.entries(q).filter(([k,v])=>!skip.has(k) && v!==null && typeof v!=='object');

  // News filtered
  const newsFiltered = (lastData.m || []).filter(x=>{
    const txt = (x.h + ' ' + x.c + ' ' + x.t).toUpperCase();
    if(nFilter==='ENERGY') return /OIL|BRENT|WTI|OPEC|CRUDE|ENERGY|GAS|COMMODIT/.test(txt);
    if(nFilter==='MACRO') return /FED|RATE|GDP|INFLATION|CPI|TREASURY|YIELD|BOJ|ECONOMY|BANK/.test(txt);
    if(nFilter==='RISK') return parseFloat(x.r||0) >= 5.0;
    if(nFilter==='BANKING') return /BANK|CREDIT|JPM|GS|FINANCE|LIQUIDITY/.test(txt);
    if(nFilter==='COMPANIES') return /NVDA|AAPL|MSFT|TECH|AI|EARNINGS|CORP|STOCK/.test(txt);
    if(nFilter==='MARKETS') return /MARKET|INDEX|SPX|NDX|DXY|BOND|EQUIT/.test(txt);
    if(nFilter==='REGIONAL') return /LATAM|VENEZUELA|BRAZIL|MEXICO|EMERGING|REGIONAL/.test(txt);
    return true;
  });
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
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        if p_clean.startswith("/api"):
            if self.headers.get("X-M82-Token") != TOK and f"token={TOK}" not in self.path:
                self.send_response(401); self.end_headers(); self.wfile.write(b"UNAUTHORIZED"); return
            payload = json.dumps(state()).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(payload))); self.end_headers(); self.wfile.write(payload); return
        body = HTML.encode()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass

HTTPServer.allow_reuse_address = True
HTTPServer(("0.0.0.0", 8282), M82MobileRequestHandler).serve_forever()
