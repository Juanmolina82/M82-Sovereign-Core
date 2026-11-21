#!/usr/bin/env python3
"""
M82 WIRE (:8282) + SOVEREIGN AI (:8285) UNIFIED COCKPIT INTEGRATOR
Respalda e inyecta el panel de consulta Air-Gapped directamente en M82 Wire.
"""
import re
import glob
import shutil
from pathlib import Path

M82_DIR = Path.home() / "M82"

# 1. Habilitar CORS en m82_sovereign_web.py (:8285) para llamadas directas desde :8282
web_py = M82_DIR / "m82_sovereign_web.py"
if web_py.exists():
    code = web_py.read_text(encoding="utf-8")
    if "Access-Control-Allow-Origin" not in code:
        code = code.replace(
            'self.send_header("Content-Type", "application/json; charset=utf-8")',
            'self.send_header("Content-Type", "application/json; charset=utf-8")\n        self.send_header("Access-Control-Allow-Origin", "*")'
        )
        options_handler = """    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):"""
        code = code.replace("    def do_GET(self):", options_handler, 1)
        web_py.write_text(code, encoding="utf-8")
        print("[+] CORS habilitado en m82_sovereign_web.py (:8285)")

# 2. Snippet embebido en M82 Wire (:8282)
WIDGET_HTML = """
<!-- M82 SOVEREIGN AI EMBEDDED WIDGET -->
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
<!-- END M82 SOVEREIGN AI EMBEDDED WIDGET -->
"""

# 3. Buscar archivos de M82 Wire (:8282) en ~/M82 y subcarpetas
candidates = []
for path_str in glob.glob(str(M82_DIR / "**" / "*"), recursive=True):
    p = Path(path_str)
    if p.is_file() and p.suffix in {".py", ".html"} and p.name not in {"m82_sovereign_web.py", "integrate_wire_ai.py"}:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        if "8282" in txt or "M82 WIRE" in txt.upper() or "M82_WIRE" in txt.upper():
            candidates.append(p)

injected = 0
for target in candidates:
    txt = target.read_text(encoding="utf-8", errors="ignore")
    if "m82-sovereign-ai-box" in txt:
        print(f"[=] Ya integrado previamente en: {target}")
        injected += 1
        continue
    if "</body>" in txt:
        shutil.copy2(target, str(target) + ".bak_ai")
        new_txt = txt.replace("</body>", WIDGET_HTML + "\n</body>", 1)
        target.write_text(new_txt, encoding="utf-8")
        print(f"[+] Integrado con respaldo (.bak_ai) en: {target}")
        injected += 1

if injected == 0:
    print("[!] No se detecto </body> estatico en :8282; lista de archivos candidatos encontrados:")
    for c in candidates:
        print("   ->", c)
