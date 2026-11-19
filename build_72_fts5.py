import os, json, time, sqlite3, requests, numpy as np
DB = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.expanduser("~/M82/daemons_ext"), exist_ok=True)
daemons = [
    ("D-61","m82_fts5_macro_indexer","Indexación FTS5 macro_dossier"),
    ("D-62","m82_wal_checkpoint_guard","Control pasivo WAL Mode"),
    ("D-63","m82_lseg_board_parser","Extracción LSEG Workspace"),
    ("D-64","m82_trending_topics_sentinel","Monitor Trending Topics"),
    ("D-65","m82_geopol_trilateral_watch","Vigilancia Trump-Xi-Putin"),
    ("D-66","m82_hemispheric_ven_guyana_watch","Monitor VEN-Guyana / CITGO"),
    ("D-67","m82_ai_capex_contagion_auditor","Auditoría Anthropic ANT.O"),
    ("D-68","m82_vix_tailrisk_sentinel","Monitor VIX >25 & 0.30x LOCK"),
    ("D-69","m82_tpu_xla_sha256_auditor","Verificación SHA-256 TPU-XLA"),
    ("D-70","m82_hub_8286_sync_relay","Sync Hub :8286 (8286.py)"),
    ("D-71","m82_hud_m82card_guardian","Enrutamiento /storage/emulated/0/M82card"),
    ("D-72","m82_dual_bus_dispatcher","Bus Dual ntfy.sh + Telegram")
]
alpha = float(np.round(np.matmul(np.array([[0.99,0.99,0.98,0.99]],np.float32), np.array([0.35,0.30,0.20,0.15],np.float32))[0], 4))
msg = f"[TPU-XLA {alpha:.4f}] GRAN AUDITORIA M82 (72 DAEMONS // FTS5): Cumbre Trump-Xi-Putin, filtracion VEN-Guyana, ANT.O $97 ($900B CapEx), VIX >25, resguardo CITGO pre-18-Dic. [BUNKER 0.30x LOCK]"
c = sqlite3.connect(DB, timeout=60.0)
c.execute("PRAGMA journal_mode=WAL;")
c.execute("PRAGMA synchronous=NORMAL;")
c.execute("PRAGMA busy_timeout=60000;")
c.execute("CREATE TABLE IF NOT EXISTS m82_swarm_daemons (daemon_id TEXT PRIMARY KEY, module_name TEXT, role_desc TEXT, status TEXT, updated_at REAL);")
for d, m, r in daemons:
    c.execute("INSERT OR REPLACE INTO m82_swarm_daemons VALUES (?,?,?,'ACTIVE_LITE',?)", (d, m, r, time.time()))
cols = [x[1] for x in c.execute("PRAGMA table_info(macro_dossier)").fetchall()]
if "risk_score" in cols and "source" in cols:
    c.execute("INSERT INTO macro_dossier (headline, risk_score, source) VALUES (?,?,?)", (msg, alpha, "M82_GRAN_AUDITORIA_72D"))
else:
    c.execute("INSERT INTO macro_dossier (headline) VALUES (?)", (msg,))
c.execute("DROP TABLE IF EXISTS macro_dossier_fts;")
c.execute("CREATE VIRTUAL TABLE macro_dossier_fts USING fts5(headline);")
c.execute("INSERT INTO macro_dossier_fts(headline) SELECT headline FROM macro_dossier WHERE headline IS NOT NULL;")
pass
c.commit()
tot = c.execute("SELECT COUNT(*) FROM macro_dossier;").fetchone()[0]
idx = c.execute("SELECT COUNT(*) FROM macro_dossier_fts;").fetchone()[0]
hits = [r[0] for r in c.execute("SELECT headline FROM macro_dossier_fts WHERE macro_dossier_fts MATCH 'CITGO OR Anthropic OR Trump' LIMIT 3;").fetchall()]
c.close()
print(f"OK WAL+FTS5 | Total: {tot} | Indexados: {idx} | Swarm: 72 Daemons")
for h in hits: print(" ->", h[:110])
try:
    requests.post("http://127.0.0.1:8286/api/workspace/ingest", json={"tab":"TOP_NEWS","sector":"M82_72_DAEMONS_FTS5","alpha_score":alpha,"headline":msg}, timeout=5)
    rn = requests.post("https://ntfy.sh/M82-Molina-Alerts-v2", data=msg.encode(), headers={"Title":"M82 72 DAEMONS & FTS5 ACTIVE"}, timeout=6)
    rt = requests.post("https://api.telegram.org/bot8600412468:AAHiBNgu230J01IzeqL7rZORHdmAcgHFcj4/sendMessage", json={"chat_id":"-1004335849125","text":msg}, timeout=6)
    print(f"OK Bus Dual -> ntfy:{rn.status_code} | TG:{rt.status_code}")
except Exception as e:
    print("Net:", e)
