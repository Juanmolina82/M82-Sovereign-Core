import os, sqlite3, html
p = os.path.expanduser("~/M82/orchestrator/m82_mobile_gateway.py")
g = open(p).read()
code = '''
        if p_clean.startswith("/dispatch/"):
            did = p_clean.split("/dispatch/")[-1]
            c = sqlite3.connect("file:"+os.path.expanduser("~/M82/m82_orchestrator_wal.db")+"?mode=ro", uri=True)
            cur = c.cursor()
            t = next((r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'") if any(k in r[0].lower() for k in ("news","wire","event","feed","dispatch","log"))), None)
            r = cur.execute(f"SELECT * FROM {t} WHERE rowid=?", (did,)).fetchone() or cur.execute(f"SELECT * FROM {t} ORDER BY rowid DESC LIMIT 1").fetchone() if t else None
            c.close()
            ts, tit, bod = (str(r[1]), str(r[2]), str(r[3]) if len(r)>3 and r[3] else str(r[2])) if r and len(r)>2 else ("LIVE UTC", "M82 DISPATCH", "Despacho sincronizado.")
            pg = f"<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content=width=device-width,initial-scale=1></head><body style=background:#07090d;color:#e2e8f0;font-family:monospace;padding:14px><div style=background:#991b1b;color:#fff;padding:10px;border-radius:8px;font-weight:700>🔴 M82 DISPATCH #{html.escape(did)}</div><div style=color:#38bdf8;font-size:11px;margin:8px 0>⏱ {html.escape(ts)} | 🔒 BUNKER 0.30x LOCK</div><div style=background:#0f172a;border:1px solid #1e293b;border-radius:10px;padding:14px;line-height:1.5;font-size:15px><strong>{html.escape(tit)}</strong><p style=color:#cbd5e1>{html.escape(bod)}</p></div><a href=/ style=display:block;text-align:center;margin-top:16px;background:#1e90ff;color:#fff;text-decoration:none;padding:12px;border-radius:8px;font-weight:700>← Volver al Terminal M82</a></body></html>".encode()
            self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(pg))); self.end_headers(); self.wfile.write(pg); return
'''
if "/dispatch/" not in g:
    g = "import sqlite3, html\n" + g.replace('p_clean = self.path.split("?")[0]', 'p_clean = self.path.split("?")[0]' + code, 1)
    open(p, "w").write(g)
print("[M82 PATCH OK]")
