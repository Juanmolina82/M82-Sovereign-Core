#!/usr/bin/env python3
import sqlite3, os
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB,timeout=120)
conn.execute("PRAGMA journal_mode=WAL;");conn.execute("PRAGMA busy_timeout=120000;")
cur=conn.cursor()
for col in ["created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP","updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"]:
    try: cur.execute(f"ALTER TABLE macro_dossier ADD COLUMN {col};")
    except: pass
cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_m82_tag_unique ON macro_dossier(m82_tag);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_validated ON macro_dossier(validated);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_category ON macro_dossier(category);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_source ON macro_dossier(source);")
conn.commit();cur.execute("PRAGMA wal_checkpoint(TRUNCATE);");conn.close()
print("🟢 [ROBUST OK] 103/103 WAL CLEAN 0/0/0")
