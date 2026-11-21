
def _m82_live_banner():
    try:
        import sqlite3 as _s
        _c = _s.connect("file:/data/data/com.termux/files/home/M82/m82_database.db?mode=ro", uri=True, timeout=15.0)
        _r = _c.execute("SELECT btc_price, btc_chg_pct, merey16_price, wti_price, wti_chg_pct, brent_price FROM m82_live_market_quotes WHERE id=1").fetchone()
        _c.close()
        if _r and _r[0]:
            return f"BTC: ${_r[0]:,.0f} ({_r[1]:+.2f}%) | MEREY 16: ${_r[2]:.2f} | WTI: ${_r[3]:.2f} | BRENT: ${_r[5]:.2f}"
    except Exception:
        pass
    return "BTC: LIVE | MEREY 16: LIVE | WTI: LIVE | BRENT: LIVE"

import os, re
p = os.path.expanduser("~/M82/orch.py")
code = open(p).read()

# 2a. Quitar cualquier precio quemado viejo que quede
code = code.replace("BRENT: $112.92", "BRENT: {brent}")
code = code.replace("BRENT: $94.32 LIVE (-4.07%)", "BRENT: {brent}")
code = code.replace(_m82_live_banner(), _m82_live_banner())
code = code.replace(_m82_live_banner(), _m82_live_banner())

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
