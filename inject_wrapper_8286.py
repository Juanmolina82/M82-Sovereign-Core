#!/usr/bin/env python3
from pathlib import Path

GW = Path.home() / "M82" / "orchestrator" / "m82_mobile_gateway.py"
txt = GW.read_text(encoding="utf-8", errors="ignore")

# Restaurar backup limpio si existe para evitar parches parciales acumulados
bak = Path(str(GW) + ".bak_clean")
if bak.exists():
    txt = bak.read_text(encoding="utf-8", errors="ignore")

INJECT_FN = '''
def _m82_inject_exec_hud(raw_bytes):
    try:
        html = raw_bytes.decode("utf-8", errors="ignore")
        if "</body>" not in html or "m82-exec-hud-v2" in html:
            return raw_bytes
        hud = """
<style id="m82-exec-hud-v2">
  #m82-exec-dock { position: sticky; top: 0; z-index: 9998; background: #0a101e; border-bottom: 1px solid #1e3a8a; padding: 8px 10px; box-shadow: 0 4px 14px rgba(0,0,0,0.65); font-family: -apple-system, sans-serif; }
  .m82-dock-hdr { display: flex; justify-content: space-between; align-items: center; }
  .m82-dock-title { font-size: 13px; font-weight: 700; color: #38bdf8; }
  .m82-toggle-btn { background: #1e293b; color: #f8fafc; border: 1px solid #334155; border-radius: 6px; padding: 3px 8px; font-size: 11px; }
  #m82-ny-bar { display: flex; justify-content: space-between; align-items: center; background: #050811; border: 1px solid #1e3a8a; border-radius: 6px; padding: 4px 8px; margin: 6px 0; font-family: monospace; font-size: 11px; color: #38bdf8; }
  .m82-ny-live { color: #34d399; font-weight: 700; }
  .m82-input-row { display: flex; gap: 6px; }
  #m82-wire-q { flex: 1; min-width: 0; background: #050811; color: #f8fafc; border: 1px solid #334155; border-radius: 7px; padding: 7px 9px; font-size: 12px; }
  #m82-wire-btn { background: #0284c7; color: #fff; border: none; border-radius: 7px; padding: 7px 12px; font-size: 11px; font-weight: 700; }
  #m82-wire-out { display: none; background: #050811; border: 1px solid #1e293b; border-radius: 7px; padding: 8px; margin-top: 6px; white-space: pre-wrap; font-family: monospace; font-size: 11px; color: #a7f3d0; max-height: 180px; overflow-y: auto; }
</style>
<script>
(function(){
  // 1. Ocultar lista superior "News Categories" y convertirla en menu lateral desplegable
  document.querySelectorAll("div,aside,nav,section").forEach(function(el){
    if(el.children.length>0 && el.innerText && el.innerText.trim().startsWith("News Categories") && el.offsetHeight<550){
      el.id="m82-cat-drawer";
      el.style.cssText="display:none;position:fixed;top:0;left:0;width:82%;max-width:300px;height:100vh;background:#070b14;z-index:10002;padding:16px;border-right:1px solid #1e3a8a;overflow-y:auto;";
    }
  });
  document.querySelectorAll("button,span,a,div").forEach(function(btn){
    var t=(btn.textContent||"").trim();
    if(t.startsWith("≡")||t==="☰"){
      btn.style.cursor="pointer";
      btn.addEventListener("click",function(e){
        var d=document.getElementById("m82-cat-drawer");
        if(d){e.preventDefault();d.style.display=(d.style.display==="none")?"block":"none";}
      });
    }
    if(t==="✕"||t==="×"||t==="X"){
      btn.style.cursor="pointer";
      btn.addEventListener("click",function(){
        var d=document.getElementById("m82-cat-drawer");
        if(d)d.style.display="none";
      });
    }
  });

  // 2. Insertar Dock Ejecutivo + Reloj NY arriba del todo
  var dock=document.createElement("div");
  dock.id="m82-exec-dock";
  dock.innerHTML=\'<div class="m82-dock-hdr"><span class="m82-dock-title">🏛️ M82 SOVEREIGN AI</span><button type="button" class="m82-toggle-btn" id="m82-tgl">Ocultar IA</button></div>\'+
    \'<div id="m82-ny-bar"><span id="m82-ny-clock">🗽 NY --:--:-- ET</span><span>EDGE 0.30x</span></div>\'+
    \'<div id="m82-dock-body"><div class="m82-input-row"><input id="m82-wire-q" type="text" placeholder="Consultar m82_database.db (WAL)..." onkeydown="if(event.key===\\\'Enter\\\')window.m82Ask()"><button type="button" id="m82-wire-btn" onclick="window.m82Ask()">ANALIZAR</button></div><pre id="m82-wire-out"></pre></div>\';
  document.body.insertBefore(dock, document.body.firstChild);

  document.getElementById("m82-tgl").onclick=function(){
    var b=document.getElementById("m82-dock-body");
    var h=b.style.display==="none";
    b.style.display=h?"block":"none";
    this.textContent=h?"Ocultar IA":"Abrir IA";
  };

  function tickNY(){
    var now=new Date();
    var t=now.toLocaleTimeString("en-US",{timeZone:"America/New_York",hour12:false,hour:"2-digit",minute:"2-digit",second:"2-digit"});
    var d=now.toLocaleDateString("en-US",{timeZone:"America/New_York",month:"short",day:"2-digit"});
    var hh=parseInt(now.toLocaleTimeString("en-US",{timeZone:"America/New_York",hour12:false,hour:"2-digit"}),10);
    var mm=parseInt(now.toLocaleTimeString("en-US",{timeZone:"America/New_York",minute:"2-digit"}),10);
    var wd=now.toLocaleDateString("en-US",{timeZone:"America/New_York",weekday:"short"});
    var mins=hh*60+mm, sess="CLOSED";
    if(wd!=="Sat"&&wd!=="Sun"){
      if(mins>=570&&mins<960)sess="NYSE/NYMEX OPEN";
      else if(mins>=240&&mins<570)sess="PRE-MARKET";
      else if(mins>=960&&mins<1200)sess="AFTER-HOURS";
    }
    document.getElementById("m82-ny-clock").innerHTML="🗽 NY "+d+" <b>"+t+" ET</b> · <span class=\\"m82-ny-live\\">"+sess+"</span>";
  }
  tickNY(); setInterval(tickNY,1000);

  window.m82Ask=async function(){
    var q=document.getElementById("m82-wire-q").value.trim();
    if(!q)return;
    var out=document.getElementById("m82-wire-out"), btn=document.getElementById("m82-wire-btn");
    out.style.display="block"; btn.disabled=true; out.textContent="⏳ Consultando nodo local (:8285)...";
    try{
      var r=await fetch("/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({q:q})});
      var j=await r.json();
      out.textContent=j.answer||j.error||"Sin respuesta.";
    }catch(e){out.textContent="Error: "+e;}
    btn.disabled=false;
  };
})();
</script>
"""
        return html.replace("</body>", hud + "\n</body>", 1).encode("utf-8")
    except Exception:
        return raw_bytes
'''

if "_m82_inject_exec_hud" not in txt:
    txt = INJECT_FN + "\n" + txt
    txt = txt.replace("self.wfile.write(body)", "self.wfile.write(_m82_inject_exec_hud(body))")
    txt = txt.replace("self.wfile.write(html.encode", "self.wfile.write(_m82_inject_exec_hud(html.encode")
    txt = txt.replace("self.wfile.write(out)", "self.wfile.write(_m82_inject_exec_hud(out))")

compile(txt, str(GW), "exec")
GW.write_text(txt, encoding="utf-8")
print("[+] HUD Ejecutivo + Reloj NY + Drawer Off-Canvas inyectados en wfile.write OK")
