#!/usr/bin/env python3
import re, shutil
from pathlib import Path

GW = Path.home() / "M82" / "orchestrator" / "m82_mobile_gateway.py"
shutil.copy2(GW, str(GW) + ".bak_clean")
txt = GW.read_text(encoding="utf-8", errors="ignore")

# 1. Asegurar ThreadingHTTPServer concurrente
txt = txt.replace(
    "from http.server import HTTPServer, BaseHTTPRequestHandler",
    "from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler"
)
txt = txt.replace("HTTPServer.allow_reuse_address", "ThreadingHTTPServer.allow_reuse_address")
txt = txt.replace('HTTPServer(("0.0.0.0", 8286)', 'ThreadingHTTPServer(("0.0.0.0", 8286)')

# 2. CSS + JS para ocultar "News Categories" arriba y abrirlo solo como drawer lateral
DRAWER_AND_DOCK = """
<style id="m82-clean-layout">
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: #070b14; color: #e2e8f0; }
  #m82-exec-dock {
    position: sticky; top: 0; z-index: 9998;
    background: rgba(10, 16, 30, 0.97); backdrop-filter: blur(8px);
    border-bottom: 1px solid #1e3a8a; padding: 10px 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.6);
  }
  .m82-dock-hdr { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
  .m82-dock-title { font-size: 13px; font-weight: 700; color: #38bdf8; letter-spacing: 0.3px; }
  .m82-badge { background: #1e1b4b; color: #a5b4fc; border: 1px solid #4338ca; padding: 2px 7px; border-radius: 999px; font-size: 10px; font-weight: 600; }
  .m82-toggle-btn { background: #1e293b; color: #f8fafc; border: 1px solid #334155; border-radius: 6px; padding: 4px 9px; font-size: 11px; cursor: pointer; }
  #m82-dock-body { margin-top: 8px; }
  .m82-chips { display: flex; gap: 6px; overflow-x: auto; padding-bottom: 6px; scrollbar-width: none; }
  .m82-chip { white-space: nowrap; background: #0f172a; color: #cbd5e1; border: 1px solid #334155; border-radius: 999px; padding: 4px 10px; font-size: 11px; cursor: pointer; }
  .m82-input-row { display: flex; gap: 6px; }
  #m82-wire-q { flex: 1; min-width: 0; background: #050811; color: #f8fafc; border: 1px solid #334155; border-radius: 8px; padding: 8px 10px; font-size: 13px; outline: none; }
  #m82-wire-btn { background: #0284c7; color: #fff; border: none; border-radius: 8px; padding: 8px 14px; font-size: 12px; font-weight: 700; cursor: pointer; }
  #m82-wire-out {
    display: none; background: #050811; border: 1px solid #1e293b; border-radius: 8px;
    padding: 9px 10px; margin-top: 8px; white-space: pre-wrap; font-family: ui-monospace, monospace;
    font-size: 12px; line-height: 1.45; color: #a7f3d0; max-height: 220px; overflow-y: auto;
  }
</style>
<script>
function m82ToggleDock(){
  const b = document.getElementById('m82-dock-body');
  const l = document.getElementById('m82-tgl-lbl');
  const hidden = b.style.display === 'none';
  b.style.display = hidden ? 'block' : 'none';
  l.textContent = hidden ? 'Ocultar' : 'Abrir IA';
}
async function m82WireAsk(preset){
  const inp = document.getElementById('m82-wire-q');
  if(preset) inp.value = preset;
  const q = inp.value.trim();
  if(!q) return;
  const btn = document.getElementById('m82-wire-btn');
  const out = document.getElementById('m82-wire-out');
  out.style.display = 'block';
  btn.disabled = true;
  btn.textContent = '...';
  out.textContent = '⏳ Inferencia local en Nodo Charallave Edge...';
  try {
    const r = await fetch('/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({q})
    });
    const d = await r.json();
    out.textContent = d.answer || d.error || 'Sin respuesta.';
  } catch(e) {
    out.textContent = 'Error de conexión: ' + e;
  }
  btn.disabled = false;
  btn.textContent = 'ANALIZAR';
}
document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll("div, aside, nav, section").forEach(function(el) {
    if (el.children.length > 0 && el.innerText && el.innerText.trim().startsWith("News Categories")) {
      if (el.offsetHeight < 550) {
        el.style.display = "none";
        el.style.position = "fixed";
        el.style.top = "0";
        el.style.left = "0";
        el.style.width = "82%";
        el.style.maxWidth = "310px";
        el.style.height = "100vh";
        el.style.background = "#070b14";
        el.style.zIndex = "10001";
        el.style.padding = "16px";
        el.style.borderRight = "1px solid #1e3a8a";
        el.style.overflowY = "auto";
        window.__m82CatDrawer = el;
      }
    }
  });
  document.querySelectorAll("button, span, a, div").forEach(function(btn) {
    const t = (btn.textContent || "").trim();
    if (t.startsWith("≡") || t === "☰") {
      btn.style.cursor = "pointer";
      btn.addEventListener("click", function(e) {
        if (window.__m82CatDrawer) {
          e.preventDefault();
          const d = window.__m82CatDrawer;
          d.style.display = (d.style.display === "none") ? "block" : "none";
        }
      });
    }
    if (t === "✕" || t === "×" || t === "X") {
      btn.style.cursor = "pointer";
      btn.addEventListener("click", function() {
        if (window.__m82CatDrawer) window.__m82CatDrawer.style.display = "none";
      });
    }
  });
});
</script>
"""

DOCK_HTML = """
<div id="m82-exec-dock">
  <div class="m82-dock-hdr">
    <span class="m82-dock-title">🏛️ M82 SOVEREIGN AI</span>
    <div style="display:flex;align-items:center;gap:6px;">
      <span class="m82-badge">🔒 BUNKER 0.30x</span>
      <button type="button" class="m82-toggle-btn" onclick="m82ToggleDock()" id="m82-tgl-lbl">Ocultar</button>
    </div>
  </div>
  <div id="m82-dock-body">
    <div class="m82-chips">
      <button type="button" class="m82-chip" onclick="m82WireAsk('Resume macro_dossier y confirma exposicion 0.22x')">📊 Macro & 0.22x</button>
      <button type="button" class="m82-chip" onclick="m82WireAsk('Analiza crudo, crack spreads y geopolitica en m82_database.db')">🛢️ Crudo & Spreads</button>
      <button type="button" class="m82-chip" onclick="m82WireAsk('Estado actual de VaR, Warsh Spread y Custodia Pasiva')">🛡️ VaR & Warsh</button>
    </div>
    <div class="m82-input-row">
      <input id="m82-wire-q" type="text" placeholder="Consultar m82_database.db (WAL)..." onkeydown="if(event.key==='Enter')m82WireAsk()">
      <button type="button" id="m82-wire-btn" onclick="m82WireAsk()">ANALIZAR</button>
    </div>
    <pre id="m82-wire-out"></pre>
  </div>
</div>
"""

if "m82-clean-layout" not in txt:
    txt = re.sub(r"(</head>)", DRAWER_AND_DOCK + r"\n\1", txt, count=1, flags=re.I)

if "m82-exec-dock" not in txt:
    txt = re.sub(r"(<body[^>]*>)", r"\1\n" + DOCK_HTML, txt, count=1, flags=re.I)

compile(txt, str(GW), "exec")
GW.write_text(txt, encoding="utf-8")
print("[+] PASO 1 COMPLETADO: UI limpia + Off-Canvas Drawer aplicados OK")
