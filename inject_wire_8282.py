#!/usr/bin/env python3
import shutil
from pathlib import Path

ORCH = Path.home() / "M82" / "orchestrator"
PROXY_PY = ORCH / "m82_8282_instant_proxy.py"
GW_PY = ORCH / "run_gateway_8283.py"

WIDGET_HTML = """<!-- M82 SOVEREIGN AI EMBEDDED WIDGET -->
<div id="m82-sovereign-ai-box" style="background:#0f172a;border:1px solid #1e3a8a;border-radius:10px;padding:14px;margin:14px auto;max-width:960px;font-family:monospace;color:#e2e8f0;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
    <strong style="color:#38bdf8;font-size:14px;">🏛️ M82 SOVEREIGN AI (WAL DB • 100% AIR-GAPPED)</strong>
    <span style="background:#1e1b4b;color:#a5b4fc;border:1px solid #4338ca;padding:2px 7px;border-radius:5px;font-size:11px;">🔒 BUNKER 0.30x LOCK</span>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px;">
    <button type="button" onclick="m82WireAsk('Analiza los ultimos eventos de macro_dossier y confirma si mantenemos 0.22x de exposicion')" style="background:#1e293b;color:#cbd5e1;border:1px solid #334155;border-radius:6px;padding:5px 9px;font-size:11px;cursor:pointer;">📊 Macro Dossier & 0.22x</button>
    <button type="button" onclick="m82WireAsk('Evalua los riesgos de crudo, crack spreads y geopolitica actuales en m82_database.db')" style="background:#1e293b;color:#cbd5e1;border:1px solid #334155;border-radius:6px;padding:5px 9px;font-size:11px;cursor:pointer;">🛢️ Crudo & Crack Spreads</button>
    <button type="button" onclick="m82WireAsk('Resume nuestra postura de riesgo, VaR y Warsh Spread bajo Custodia Pasiva')" style="background:#1e293b;color:#cbd5e1;border:1px solid #334155;border-radius:6px;padding:5px 9px;font-size:11px;cursor:pointer;">🛡️ VaR & Warsh Spread</button>
  </div>
  <div style="display:flex;gap:8px;">
    <input id="m82-wire-q" type="text" placeholder="Consultar m82_database.db sin internet..." style="flex:1;background:#090d16;color:#f8fafc;border:1px solid #334155;border-radius:6px;padding:9px;font-size:13px;" onkeydown="if(event.key==='Enter')m82WireAsk()">
    <button type="button" id="m82-wire-btn" onclick="m82WireAsk()" style="background:#0284c7;color:#fff;border:none;border-radius:6px;padding:9px 14px;font-weight:bold;cursor:pointer;">ANALIZAR</button>
  </div>
  <pre id="m82-wire-out" style="background:#060911;border:1px solid #1e293b;border-radius:6px;padding:10px;margin-top:9px;white-space:pre-wrap;font-size:12px;color:#a7f3d0;min-height:44px;">Listo. Consulte su base de datos M82 directamente desde M82 Wire.</pre>
</div>
<script>
async function m82WireAsk(preset){
  const inp = document.getElementById('m82-wire-q');
  if(preset) inp.value = preset;
  const q = inp.value.trim();
  if(!q) return;
  const btn = document.getElementById('m82-wire-btn');
  const out = document.getElementById('m82-wire-out');
  btn.disabled = true;
  out.textContent = "⏳ Procesando inferencia local en Nodo Charallave Edge (espere ~15-30s)...";
  try {
    const r = await fetch('http://127.0.0.1:8285/ask', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({q})
    });
    const d = await r.json();
    out.textContent = d.answer || d.error || "Sin respuesta.";
  } catch(e) {
    out.textContent = "Error conectando al worker local (:8285): " + e;
  }
  btn.disabled = false;
}
</script>
<!-- END M82 SOVEREIGN AI EMBEDDED WIDGET -->"""

# 1. Intentar inyectar en run_gateway_8283.py o en el HTML que referencie
for f in [GW_PY, PROXY_PY]:
    if f.exists():
        txt = f.read_text(encoding="utf-8", errors="ignore")
        if "m82-sovereign-ai-box" in txt:
            print(f"[=] Ya inyectado en {f.name}")
            continue
        for tag in ("</body>", "</BODY>", "</html>", "</HTML>"):
            if tag in txt:
                shutil.copy2(f, str(f) + ".bak_ai")
                f.write_text(txt.replace(tag, WIDGET_HTML + "\n" + tag, 1), encoding="utf-8")
                print(f"[+] Inyectado directamente en {f.name}")
                break

# 2. Si el HTML viene del proxy bytes en Instant8282Handler, parchear envio de body HTML
ptxt = PROXY_PY.read_text(encoding="utf-8", errors="ignore")
if "m82-sovereign-ai-box" not in ptxt and "self.wfile.write(" in ptxt:
    shutil.copy2(PROXY_PY, str(PROXY_PY) + ".bak_ai")
    hook = (
        f"WIDGET_BYTES = {repr(WIDGET_HTML.encode('utf-8'))}\n"
        "def _inject_ai(b):\n"
        "    if isinstance(b, bytes) and b'</body>' in b and b'm82-sovereign-ai-box' not in b:\n"
        "        return b.replace(b'</body>', WIDGET_BYTES + b'</body>', 1)\n"
        "    return b\n"
    )
    ptxt = hook + ptxt.replace("self.wfile.write(body)", "self.wfile.write(_inject_ai(body))").replace("self.wfile.write(data)", "self.wfile.write(_inject_ai(data))")
    PROXY_PY.write_text(ptxt, encoding="utf-8")
    print("[+] Hook de bytes HTML inyectado en Instant8282Handler (:8282)")
