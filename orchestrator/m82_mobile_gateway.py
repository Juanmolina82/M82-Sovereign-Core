#!/usr/bin/env python3
import os, json, sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
ROOT = os.path.expanduser("~/M82")
def state():
    d = {"q": {}, "n": [], "a": []}
    for fn, dbn, sql, k in [
        (1, "m82_orchestrator_wal.db", "SELECT payload_json FROM m82_refinitiv_feed_ledger ORDER BY captured_at DESC LIMIT 1", "q"),
        (2, "m82_database.db", "SELECT source, category, headline, risk_score, m82_tag, created_at FROM macro_dossier ORDER BY id DESC LIMIT 10", "n"),
        (3, "m82_database.db", "SELECT event_type, headline, risk_score FROM m82_tail_risk_alerts ORDER BY id DESC LIMIT 5", "a")
    ]:
        try:
            c = sqlite3.connect(os.path.join(ROOT, dbn), timeout=30)
            c.execute("PRAGMA journal_mode=WAL;"); c.execute("PRAGMA busy_timeout=60000;")
            rows = c.execute(sql).fetchall(); c.close()
            if fn == 1 and rows: d["q"] = json.loads(rows[0][0])
            elif fn == 2: d["n"] = [{"s":r[0],"c":r[1],"h":r[2],"r":r[3],"t":r[4],"ts":r[5]} for r in rows]
            elif fn == 3: d["a"] = [{"t":r[0],"h":r[1],"r":r[2]} for r in rows]
        except Exception: pass
    return d
HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#000000"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{box-sizing:border-box;margin:0;padding:0;font-family:sans-serif}body{background:#000;color:#fff;padding-bottom:88px}
.top{position:sticky;top:0;background:#000;border-bottom:1px solid #222;padding:12px;display:flex;justify-content:space-between;align-items:center}
.b{background:#2a080d;border:1px solid #ff1744;color:#ff5252;font-size:10px;padding:3px 7px;border-radius:4px;font-weight:700}
.ban{background:linear-gradient(135deg,#b71c1c,#e53935);padding:16px}.ban h2{font-size:26px;font-weight:900}
.card{padding:12px;border-bottom:1px solid #181818}.card h3{font-size:17px;line-height:1.3;margin:4px 0}
.tag{color:#1e90ff;font-size:11px;font-weight:700;border:1px solid #1e90ff55;padding:2px 6px;border-radius:3px;display:inline-block;margin-top:6px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:12px}.box{background:#0c0c0c;border:1px solid #222;border-radius:8px;padding:12px}
.tk{position:fixed;bottom:52px;left:0;right:0;background:#0a0a0a;border-top:1px solid #222;padding:6px 10px;font-size:11px;display:flex;justify-content:space-between;color:#00e676;font-weight:700}
.nav{position:fixed;bottom:0;left:0;right:0;height:52px;background:#050505;display:flex;justify-content:space-around;align-items:center}
.nav button{background:none;border:none;color:#777;font-size:11px;font-weight:700}.nav button.act{color:#1e90ff}.tab{display:none}.tab.act{display:block}
</style>
<style id="m82-ticker-style">
.m82-tape-wrap{width:100%;overflow:hidden;background:#0a0e17;border-top:1px solid #1b2838;border-bottom:1px solid #1b2838;padding:6px 0;white-space:nowrap;position:relative;}
.m82-tape-track{display:inline-block;padding-left:100%;animation:m82scroll 38s linear infinite;font-family:monospace;font-size:12px;letter-spacing:0.4px;color:#cbd5e1;}
.m82-tape-wrap:hover .m82-tape-track,.m82-tape-wrap:active .m82-tape-track{animation-play-state:paused;}
.m82-t-sym{color:#38bdf8;font-weight:700;margin-left:18px;}
.m82-t-up{color:#10b981;font-weight:600;}
.m82-t-dn{color:#ef4444;font-weight:600;}
.m82-t-lock{color:#f59e0b;font-weight:700;margin-left:18px;}
@keyframes m82scroll{0%{transform:translate3d(0,0,0);}100%{transform:translate3d(-100%,0,0);}}
</style>

</head><body>
<div class="top"><strong style="color:#1e90ff">M82 QUANTUM WIRE</strong><span class="b">BUNKER 0.30x LOCK</span></div>
<div id="t-n" class="tab act"><div class="ban"><h2>M82 breaking wire</h2><small>M82 SOVEREIGN WIRE / M82 SOVEREIGN WIRE &bull;</small></div>

<div class="m82-tape-wrap" title="Toque para pausar lectura">
  <div class="m82-tape-track" id="m82-tape">
    <span class="m82-t-lock">🔒 BUNKER 0.30x LOCK</span>
    <span class="m82-t-sym">EXP:</span> 0.22x | <span class="m82-t-sym">DRY POWDER:</span> 78.0% | <span class="m82-t-sym">VaR:</span> 1.68% | <span class="m82-t-sym">WARSH SPREAD:</span> 102.0 bps
    <span class="m82-t-sym">WTI</span> <span class="m82-t-up">$68.42 (+0.45%)</span>
    <span class="m82-t-sym">BRENT</span> <span class="m82-t-up">$72.18 (+0.38%)</span>
    <span class="m82-t-sym">CRACK 3-2-1</span> <span class="m82-t-up">$21.65</span>
    <span class="m82-t-sym">US 10Y</span> <span class="m82-t-dn">4.42%</span>
    <span class="m82-t-sym">DXY</span> <span class="m82-t-up">106.68</span>
    <span class="m82-t-sym">NVDA</span> <span class="m82-t-up">$144.80</span>
    <span class="m82-t-sym">BTC-USD</span> <span class="m82-t-up">$91,250</span>
  </div>
</div>
<script>
setInterval(async()=>{try{const r=await fetch('/api');const d=await r.json();const rows=(d.items||d.news||d.events||d||[]);const q=rows.filter(x=>JSON.stringify(x).includes('QUANTUM TELEMETRY')).slice(0,6);if(q.length){document.getElementById('m82-tape').innerHTML='<span class="m82-t-lock">🔒 BUNKER 0.30x LOCK | EXP 0.22x | DRY POWDER 78.0% | VaR 1.68%</span> '+q.map(x=>'<span class="m82-t-sym">•</span> '+(x.title||x.message||x.headline||JSON.stringify(x)).replace('[M82 QUANTUM TELEMETRY]','')).join(' ');}}catch(e){}},15000);
</script>
<div id="nl"></div></div>
<div id="t-m" class="tab"><div class="grid" id="mg"></div></div>
<div id="t-p" class="tab"><div class="grid"><div class="box"><small style="color:#888">EXPOSICION</small><h2>0.22x / 0.30x</h2></div><div class="box"><small style="color:#888">DRY POWDER</small><h2>78.0%</h2></div><div class="box"><small style="color:#888">VaR DIARIO</small><h2 style="color:#ffb300">1.68%</h2></div><div class="box"><small style="color:#888">WARSH SPREAD</small><h2>102.0 bps</h2></div><div class="box" style="grid-column:span 2" id="al"></div></div></div>
<div class="tk" id="tk">Cargando WAL...</div>
<div class="nav"><button onclick="sw('m',this)">Mercados</button><button onclick="sw('p',this)">Portafolio</button><button class="act" onclick="sw('n',this)">Noticias</button></div>
<script>function sw(i,b){document.querySelectorAll('.tab').forEach(e=>e.classList.remove('act'));document.querySelectorAll('.nav button').forEach(e=>e.classList.remove('act'));document.getElementById('t-'+i).classList.add('act');b.classList.add('act')}
async function ld(){const r=await fetch("/api?token=23bd5bf695350216506321df0466834b&t=23bd5bf695350216506321df0466834b", {headers: {"X-M82-Token": "23bd5bf695350216506321df0466834b"}});const d=await r.json();const q=d.q||{};
document.getElementById('tk').innerHTML=`<span>WTI $${q.CLc1||'-'}</span><span>BRENT $${q.LCOc1||'-'}</span><span>CRACK $${q.crack_321_usd||'-'}</span><span>10Y ${q['US10YT=RR']||'-'}%</span>`;
document.getElementById('nl').innerHTML=(d.n||[]).map(x=>`<div class="card"><small style="color:#888">${x.s} &bull; ${(x.ts||'').slice(0,16)}</small><h3>${x.h}</h3><small style="color:#ffb300">RISK: ${x.r}</small><br><span class="tag">${x.t}</span></div>`).join('');
document.getElementById('mg').innerHTML=[['WTI','$'+q.CLc1],['Brent','$'+q.LCOc1],['Crack 3-2-1','$'+q.crack_321_usd],['UST 10Y',q['US10YT=RR']+'%'],['DXY',q['.DXY']],['HO','$'+q.HOc1]].map(i=>`<div class="box"><small style="color:#888">${i[0]}</small><h2>${i[1]}</h2></div>`).join('');
document.getElementById('al').innerHTML=(d.a||[]).map(a=>`<div style="padding:4px 0;border-bottom:1px solid #222"><b style="color:#ff5252">[${a.r}] ${a.t}</b>: ${a.h}</div>`).join('');}
ld();setInterval(ld,15000);if("serviceWorker"in navigator)navigator.serviceWorker.register("/sw.js");</script>
<script>
document.addEventListener('click', e => {
  const card = e.target.closest('div, li, article');
  if (card && card.innerText && card.innerText.length > 25 && !e.target.closest('a, button, .m82-tape-wrap')) {
    const idAttr = card.getAttribute('data-id') || 'latest';
    window.location.href = '/dispatch/' + idAttr;
  }
});
</script>

</body></html>"""
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        p_clean = self.path.split("?")[0]
        if p_clean in ("/icon.png", "/icon-192.png", "/icon-512.png"):
            fn = "icon-512.png" if "512" in p_clean else "icon-192.png"
            data = open(os.path.expanduser("~/M82/orchestrator/" + fn), "rb").read()
            self.send_response(200); self.send_header("Content-Type", "image/png"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        if p_clean == "/manifest.json":
            mf = b'{"name":"M82 Quantum Wire","short_name":"M82 Wire","start_url":"/","display":"standalone","background_color":"#07090d","theme_color":"#07090d","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"/icon-512.png","sizes":"512x512","type":"image/png"}]}'
            self.send_response(200); self.send_header("Content-Type", "application/manifest+json"); self.send_header("Content-Length", str(len(mf))); self.end_headers(); self.wfile.write(mf); return
        if p_clean == "/sw.js":
            sw = b"self.addEventListener('install',()=>self.skipWaiting());self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));"
            self.send_response(200); self.send_header("Content-Type", "application/javascript"); self.send_header("Content-Length", str(len(sw))); self.end_headers(); self.wfile.write(sw); return

        tok=open(os.path.expanduser("~/M82/.env.gateway")).read().strip().split("=")[1]
        if self.path.startswith("/api") and self.headers.get("X-M82-Token")!=tok and f"t={tok}" not in self.path:
            self.send_response(401); self.end_headers(); self.wfile.write(b"UNAUTHORIZED"); return
        c, b = ("application/json", json.dumps(state()).encode()) if self.path.startswith("/api") else ("text/html;charset=utf-8", HTML.encode())
        self.send_response(200); self.send_header("Content-Type", c); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a): pass
HTTPServer.allow_reuse_address = True; HTTPServer(("0.0.0.0", 8282), H).serve_forever()
