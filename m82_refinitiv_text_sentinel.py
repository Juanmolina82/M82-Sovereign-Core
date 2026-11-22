import os, time, sqlite3, hashlib, datetime, xml.etree.ElementTree as ET, urllib.request
from m82_unified_wire_hud import dispatch_wire

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTHONOPTIMIZE"] = "1"

KEYWORDS = [
    "hormuz", "oman", "ukmto", "tanker", "iran", "bahrain", "corpus christi",
    "padd 3", "port", "cyber", "venezuela", "ofac", "crude", "oil", "brent", "wti", "vix"
]

FEEDS = [
    ("REUTERS_WORLD", "https://feeds.reuters.com/Reuters/worldNews"),
    ("REUTERS_BIZ", "https://feeds.reuters.com/reuters/businessNews"),
    ("EIA_ENERGY", "https://www.eia.gov/rss/todayinenergy.xml"),
]

def scan_once():
    for src, url in FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "M82-Sovereign-Core/60.5"})
            raw = urllib.request.urlopen(req, timeout=10).read()
            root = ET.fromstring(raw)
            for item in root.findall(".//item")[:8]:
                title_el = item.find("title")
                if title_el is None or not title_el.text:
                    continue
                title = title_el.text.strip()
                low = title.lower()
                if any(k in low for k in KEYWORDS):
                    q_analysis = (
                        "• Nivel VIII & X: P(Búnker | E) = 99.64% | LOCKOUT: NO TRADE 18:00 VET.\n"
                        "• Pods Blindados: Gas-to-Compute (55.93%) + Merey 16 Non-Hormuz (9.15%) | Exp. 0.22x."
                    )
                    x_post = f"WIRE ({src}): {title[:135]}. M82 mantiene BUNKER 0.30x LOCK y Dry Powder blindado ante volatilidad energética. #Energy #Macro #M82"
                    dispatch_wire(src, title, q_analysis, x_post, force=False)
        except Exception:
            pass

if __name__ == "__main__":
    print("[M82 REFINITIV TEXT SENTINEL] Iniciado en modo 100% texto limpio (cero HUD PNG)...")
    scan_once()
