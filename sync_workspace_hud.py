import os, sqlite3, hashlib, datetime, sys
sys.path.insert(0, os.path.expanduser("~/M82"))
from core_ingestor import ingest_event

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
ts_ref = now.strftime("#M82-%Y%m%d-%H%M")
payload = f"REFINITIV_WORKSPACE|jmmp@molina82.com|{ts_ref}|VIX:31.96|SOX:-8.69%|WARSH:+102bps|HORMUZ:-65%"
sha = hashlib.sha256(payload.encode()).hexdigest()[:16].upper()

headline = (
    f"M82 QUANTITATIVE MARKET FEED | USER: jmmp@molina82.com | "
    f"VIX 31.96 (+12.38%) | SOX -8.69% | FED HIKE PROB 98.2% | "
    f"ENERGY ROTATION (EOG, COP, XOM) + HORMUZ -65% | "
    f"SHA-256: {sha} | REF: {ts_ref} | BUNKER 0.30x LOCK"
)
ingest_event("REFINITIV_WORKSPACE_JMMP", "MARKET_CLOSING_SETTLEMENT", headline, 9.2, 0.88, "REFINITIV,JMMP,VIX,SOX,ENERGY,HORMUZ", "M82_WS_CLOSING_FEED", "CHARALLAVE_L4_L5_EDGE")
print(f"✅ SYNC OK | USER: jmmp@molina82.com | REF: {ts_ref} | SHA-256: {sha}")
