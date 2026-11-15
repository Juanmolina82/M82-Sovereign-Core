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
            rows = c2.execute("SELECT id, source, category, headline, risk_score, m82_tag, created_at FROM macro_dossier WHERE headline NOT LIKE '%Live Poll 20 activos%' AND headline NOT LIKE '%Multichannel Telegram%' ORDER BY id DESC LIMIT 20").fetchall()
            d["m"] = [{"id": r[0], "s": r[1], "c": r[2], "h": r[3], "r": r[4], "t": r[5], "ts": r[6]} for r in rows]
        if "m82_tail_risk_alerts" in tabs:
            rows = c2.execute("SELECT id, event_type, headline, risk_score FROM m82_tail_risk_alerts ORDER BY id DESC LIMIT 10").fetchall()
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
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{{background:#07090d;color:#e8f0fe;font-family:sans-serif;margin:0;padding:16px}}.bar{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1e293b;padding-bottom:12px;margin-bottom:16px}}.btn{{background:#111827;color:#38bdf8;border:1px solid #38bdf8;padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:700;font-size:12px}}.bunker{{background:#2a080d;border:1px solid #ff1744;color:#ff5252;padding:6px 10px;border-radius:4px;font-size:11px;font-weight:700}}.card{{background:#0d1117;border:1px solid #1f2937;border-radius:8px;padding:16px}}.meta{{color:#94a3b8;font-size:12px;margin-bottom:8px;font-family:monospace}}h1{{font-size:18px;line-height:1.4;margin:8px 0 14px;color:#fff}}.body{{font-size:14px;line-height:1.65;color:#cbd5e1;white-space:pre-wrap;border-top:1px solid #1f2937;padding-top:12px}}.tag{{display:inline-block;background:#172554;color:#60a5fa;border:1px solid #1d4ed8;padding:3px 8px;border-radius:4px;font-size:11px;font-weight:700;margin-right:6px}}</style></head><body><div class="bar"><a class="btn" href="/">&#8592; VOLVER AL WIRE</a><span class="bunker">&#128274; BUNKER 0.30x LOCK</span></div><div class="card"><div class="meta">ID #{html.escape(str(item_id))} &bull; {html.escape(source)} &bull; {html.escape(ts)}</div><div><span class="tag">{html.escape(cat)}</span><span class="tag" style="color:#fbbf24;border-color:#b45309;background:#451a03">RISK {html.escape(risk)}</span><span class="tag">{html.escape(tag)}</span></div><h1>{html.escape(title)}</h1><div class="body">{html.escape(body or title)}</div></div></body></html>"""

HTML = """<!doctype html><html><head><meta charset="utf-8"><link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#07090d"><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}body{background:#07090d;color:#fff;padding-bottom:68px}.top{position:sticky;top:0;z-index:20;background:#07090d;border-bottom:1px solid #1e293b;padding:12px;display:flex;justify-content:space-between;align-items:center}.b{background:#2a080d;border:1px solid #ff1744;color:#ff5252;padding:6px 10px;border-radius:4px;font-size:11px;font-weight:700}.ban{background:linear-gradient(135deg,#0b172c,#1e3a8a);padding:14px;border-bottom:1px solid #1e293b}.ban h2{font-size:18px;font-weight:900}.card{padding:13px;border-bottom:1px solid #1e293b;cursor:pointer}.card:active{background:#111827}.card h3{font-size:14px;line-height:1.4;margin:5px 0;color:#f8fafc}.tag{color:#60a5fa;font-size:10px;font-weight:700;border:1px solid #1d4ed8;background:#0f172a;padding:2px 6px;border-radius:3px;display:inline-block;margin-top:4px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:12px}.box{background:#0d1117;border:1px solid #1f2937;border-radius:6px;padding:11px;transition:border-color .35s,background .35s}.box.up{border-color:#00e676;background:#062016}.box.dn{border-color:#ff5252;background:#240b0e}.tk{position:fixed;bottom:52px;left:0;right:0;z-index:15;background:#0b1120;border-top:1px solid #1e293b;padding:7px 10px;font-size:11px;font-family:monospace;display:flex;justify-content:space-between;color:#38bdf8;font-weight:700}.nav{position:fixed;bottom:0;left:0;right:0;z-index:20;height:52px;background:#05070b;border-top:1px solid #1e293b;display:flex;justify-content:space-around;align-items:center}.nav button{background:none;border:none;color:#64748b;font-size:12px;font-weight:700;padding:8px 14px}.nav button.act{color:#38bdf8}.tab{display:none}.tab.act{display:block}.m82-tape-wrap{width:100%;overflow:hidden;background:#0a0f1c;border-bottom:1px solid #1e293b;padding:6px 0;white-space:nowrap;position:relative}.m82-tape-track{display:inline-block;padding-left:100%;animation:m82scroll 42s linear infinite;font-family:monospace;font-size:12px;color:#cbd5e1}.m82-tape-wrap:hover .m82-tape-track,.m82-tape-wrap:active .m82-tape-track{animation-play-state:paused}.m82-t-sym{color:#38bdf8;font-weight:700;margin-left:14px}.m82-t-up{color:#00e676;font-weight:700}.m82-t-dn{color:#ff5252;font-weight:700}.m82-t-flat{color:#e2e8f0;font-weight:700}.m82-t-lock{color:#ff5252;font-weight:700;margin-left:12px}@keyframes m82scroll{0%{transform:translate3d(0,0,0)}100%{transform:translate3d(-100%,0,0)}}</style></head><body><div class="top"><strong style="color:#38bdf8">M82 QUANTUM WIRE</strong><span class="b">&#128274; BUNKER 0.30x LOCK</span></div><div id="t-n" class="tab act"><div class="ban"><h2>M82 breaking wire</h2><small style="color:#93c5fd">M82 SOVEREIGN WIRE &bull; jmmp@molina82.com</small></div><div class="m82-tape-wrap"><div class="m82-tape-track" id="m82-tape"><span class="m82-t-lock">&#128274; BUNKER 0.30x LOCK</span><span class="m82-t-sym">SINCRONIZANDO REFINITIV WORKSPACE...</span></div></div><div id="nl"></div></div><div id="t-m" class="tab"><div class="grid" id="mg"></div></div><div id="t-p" class="tab"><div class="grid"><div class="box"><small style="color:#888">EXPOSICION</small><h2>0.22x / 0.30x</h2></div><div class="box"><small style="color:#888">DRY POWDER</small><h2 style="color:#00e676">78.0%</h2></div><div class="box"><small style="color:#888">VAR DIARIO</small><h2 style="color:#fbbf24">1.68%</h2></div><div class="box"><small style="color:#888">WARSH SPREAD</small><h2>102.0 bps</h2></div><div class="box" style="grid-column:span 2"><small style="color:#888">ALERTAS TAIL-RISK (TOCAR PARA ABRIR)</small><div id="al" style="margin-top:6px"></div></div></div></div><div class="tk" id="tk"><span>WS: jmmp@molina82.com</span><span>CARGANDO WAL...</span></div><div class="nav"><button onclick="sw('m',this)">Mercados</button><button onclick="sw('p',this)">Portafolio</button><button class="act" onclick="sw('n',this)">Noticias</button></div><script>const TOK="__TOK__";let prevQ={},dirQ={};function sw(t,b){document.querySelectorAll('.tab').forEach(e=>e.classList.remove('act'));document.getElementById('t-'+t).classList.add('act');document.querySelectorAll('.nav button').forEach(e=>e.classList.remove('act'));b.classList.add('act');}function fmtInst(k,v){if(typeof v!=='number')return String(v);const pct=new Set(['US10YT=RR','US2YT=RR','US30YT=RR','VIX','OVX','GVZ']);const idx=new Set(['DXY','.DXY','DX-Y.NYB','NQ=F','NDX','ES=F','YM=F','RTY=F','N225','^N225','GDAXI','^GDAXI','ZB=F','FM.US']);const s=v.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});if(pct.has(k)||k.includes('YT=')||k.endsWith('_pct'))return s+'%';if(idx.has(k))return s;return '$'+s;}async function ld(){try{const r=await fetch('/api?token='+TOK,{headers:{'X-M82-Token':TOK}});const d=await r.json();const q=d.q||{};const skip=new Set(['source','captured_at','user','status','ts','workspace']);const entries=Object.entries(q).filter(([k,v])=>!skip.has(k)&&v!==null&&typeof v!=='object');entries.forEach(([k,v])=>{if(typeof v==='number'&&typeof prevQ[k]==='number'){if(v>prevQ[k])dirQ[k]='up';else if(v<prevQ[k])dirQ[k]='dn';}});const tapeItems=entries.map(([k,v])=>{const st=dirQ[k]||'flat';const cls=st==='up'?'m82-t-up':(st==='dn'?'m82-t-dn':'m82-t-flat');const arr=st==='up'?' &#9650;':(st==='dn'?' &#9660;':'');return `<span class="m82-t-sym">${k}</span> <span class="${cls}">${fmtInst(k,v)}${arr}</span>`;}).join(' |');const tp=document.getElementById('m82-tape');if(tp&&entries.length){tp.innerHTML=`<span class="m82-t-lock">&#128274; BUNKER 0.30x LOCK</span><span class="m82-t-sym">WS: jmmp@molina82.com (${entries.length})</span> |${tapeItems} `;}document.getElementById('tk').innerHTML=`<span>WTI ${fmtInst('CLc1',q.CLc1||99.5)}</span><span>BRENT ${fmtInst('LCOc1',q.LCOc1||114.72)}</span><span>CRACK ${fmtInst('crack_321_usd',q.crack_321_usd||37.42)}</span><span>10Y ${fmtInst('US10YT=RR',q['US10YT=RR']||4.38)}</span>`;document.getElementById('nl').innerHTML=(d.m||[]).map(x=>`<div class="card" data-id="${x.id||'latest'}"><small style="color:#94a3b8">${x.s} &bull; ${(x.ts||'').slice(0,16)}</small><h3>${x.h}</h3><small style="color:#fbbf24">RISK ${x.r}</small> <span class="tag">${x.t}</span></div>`).join('');document.getElementById('mg').innerHTML=`<div class="box" style="grid-column:span 2;border-color:#00e676"><small style="color:#00e676">REFINITIV WORKSPACE &bull; jmmp@molina82.com</small><h2 style="font-size:14px;margin-top:4px">${entries.length} ACTIVOS REALES EN VIVO (TICK 2s WAL)</h2></div>`+entries.map(([k,v])=>{const st=dirQ[k]||'';const vCol=st==='up'?'#00e676':(st==='dn'?'#ff5252':'#f8fafc');const arr=st==='up'?' &#9650;':(st==='dn'?' &#9660;':'');return `<div class="box ${st}"><small style="color:#94a3b8">${k}</small><h2 style="color:${vCol};font-size:17px;margin-top:3px">${fmtInst(k,v)}${arr}</h2></div>`;}).join('');document.getElementById('al').innerHTML=(d.a||[]).map(a=>`<div class="card" data-id="A-${a.id||1}" style="padding:8px 0"><b style="color:#ff5252">[${a.t}]</b> ${a.h} <small style="color:#fbbf24">(${a.r})</small></div>`).join('');entries.forEach(([k,v])=>{if(typeof v==='number')prevQ[k]=v;});}catch(e){}}ld();setInterval(ld,2000);document.addEventListener('click',e=>{const card=e.target.closest('.card');if(card&&!e.target.closest('a,button,.m82-tape-wrap')){const idAttr=card.getAttribute('data-id')||'latest';window.location.href='/dispatch/'+encodeURIComponent(idAttr);}});</script></body></html>""".replace("__TOK__", TOK)

class M82MobileRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        p_clean = self.path.split("?")[0]
        if p_clean in ("/icon.png", "/icon-192.png", "/icon-512.png"):
            fn = "icon-512.png" if "512" in p_clean else "icon-192.png"
            data = open(os.path.join(ROOT, "orchestrator", fn), "rb").read()
            self.send_response(200); self.send_header("Content-Type", "image/png"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        if p_clean == "/manifest.json":
            mf = b'{"name":"M82 Quantum Wire","short_name":"M82 Wire","start_url":"/","display":"standalone","background_color":"#07090d","theme_color":"#07090d","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png"}]}'
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
