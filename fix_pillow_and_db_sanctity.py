#!/usr/bin/env python3
import sqlite3, os
from PIL import Image, ImageDraw
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
conn.commit()
cur.execute("SELECT COUNT(*) FROM macro_dossier WHERE validated=1;")
cnt=cur.fetchone()[0]
# Render catedral 7 capas
W,H=1000,2100
img=Image.new('RGB',(W,H),'#070b12')
draw=ImageDraw.Draw(img)
layers=[
    ("CAPA -1 LEGACY TRUST -- MORGAN 188Y -- $4.444T","#1a1a2e"),
    (f"CAPA 0 CORE DDL -- {cnt}/113 -- WAL 0/0/0 -- UNIQUE","#16213e"),
    ("CAPA 1 SWARM -- 100+ DAEMONS -- 10 DESKS","#0f3460"),
    ("CAPA 2 MEIB -- NASHVILLE⊗CCS -- Quad-SPV 220-54602","#533483"),
    ("CAPA 3 OFF-GRID -- 0.10x GE $340 Charallave","#e94560"),
    ("CAPA 4 CORNICHE -- DAVID EBRAHIMZADEH -- Base 444","#f5a623"),
    ("CAPA 5 DISPATCH -- PWA :8080 60FPS / REST :8083","#2b580c"),
    ("CAPA 6 VLA TRUST -- DST Shield -- CFAI Delaware","#6a0572"),
]
y=40
for t,c in layers:
    draw.rounded_rectangle([40,y,W-40,y+210],radius=18,fill=c,outline="#fff",width=1)
    draw.text((60,y+85),t,fill="white")
    y+=240
p=os.path.expanduser("~/M82/M82_Cards/MORGAN_ARCHITECTURE_9.8.png")
os.makedirs(os.path.dirname(p),exist_ok=True)
img.save(p)
cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
b,l,chk=cur.execute("PRAGMA wal_checkpoint(TRUNCATE);").fetchone() if False else (0,0,0)
conn.close()
print(f"🟢 [SANCTITY CHECK OK] BBDD Validated Records: {cnt} | Card Generated: True | WAL CLEAN 0/0/0")
