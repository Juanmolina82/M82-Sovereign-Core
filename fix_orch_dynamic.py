import os, re
p = os.path.expanduser("~/M82/orch.py")
code = open(p).read()

# 2a. Quitar cualquier precio quemado viejo que quede
code = code.replace("BRENT: $112.92", "BRENT: {brent}")
code = code.replace("BRENT: $94.32 LIVE (-4.07%)", "BRENT: {brent}")
code = code.replace("MEREY 16: $93.75 SEP / $93.92 LIVE", "MEREY 16: {merey} | WTI: {wti}")
code = code.replace("MEREY 16: $83.15 LIVE | WTI: $87.71", "MEREY 16: {merey} | WTI: {wti}")

# 2b. Inyectar loader dinamico al inicio de la funcion de render si no existe
if "commodities_live" not in code:
    loader = '''
# --- M82 DYNAMIC LOADER - Lee data.json en cada render, nunca valores quemados ---
import json as _json
def _load_live():
    try:
        with open(os.path.expanduser("~/M82/app/data.json")) as _f:
            _d = _json.load(_f)
        _c = _d.get("commodities_live", {}) if isinstance(_d, dict) else {}
        return {
            "brent": f"${_c.get('brent_lcoc1', 'N/A')} ({_c.get('brent_change_pct', '')}%)",
            "wti": f"${_c.get('wti_clc1', 'N/A')} ({_c.get('wti_change_pct', '')}%)",
            "merey": f"${_c.get('merey16_live', 'N/A')} LIVE",
        }
    except Exception as _e:
        return {"brent": "N/A", "wti": "N/A", "merey": "N/A"}
_live = _load_live()
brent, wti, merey = _live["brent"], _live["wti"], _live["merey"]
'''
    # Insertar despues de los imports
    code = code.replace("from PIL", loader + "\nfrom PIL", 1) if "from PIL" in code else loader + "\n" + code

open(p, "w").write(code)
print("[ORCH OK] orch.py ahora es DINAMICO - lee data.json en cada render.")
