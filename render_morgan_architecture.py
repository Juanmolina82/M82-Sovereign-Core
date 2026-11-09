#!/usr/bin/env python3
from PIL import Image, ImageDraw
import os
W,H=1000,2100
img=Image.new('RGB',(W,H),'#070b12')
draw=ImageDraw.Draw(img)
layers=[
    ("CAPA -1 LEGACY TRUST -- MORGAN 188Y -- Kidder/NationsBank $4.444T","#1a1a2e"),
    ("CAPA 0 CORE DDL -- 103/103 -- WAL 0/0/0 -- UNIQUE(m82_tag) MSI 1500","#16213e"),
    ("CAPA 1 SWARM -- 100+ DAEMONS -- 10 DESKS -- supervisor.sh 15s","#0f3460"),
    ("CAPA 2 MEIB -- NASHVILLE⊗CARACAS -- Quad-SPV JMM Exp 220-54602","#533483"),
    ("CAPA 3 OFF-GRID -- 0.10x GAS-TO-COMPUTE -- GE $340 Charallave","#e94560"),
    ("CAPA 4 CORNICHE -- DAVID EBRAHIMZADEH -- 50/50 -- Base 444","#f5a623"),
    ("CAPA 5 DISPATCH -- PWA :8080 60FPS / REST :8083 / Telegram","#2b580c"),
    ("CAPA 6 VLA TRUST FOUNDATION -- DST Shield -- CFAI -- Delaware","#6a0572"),
]
y=40
for title,color in layers:
    draw.rounded_rectangle([40,y,W-40,y+210],radius=18,fill=color,outline="#fff",width=1)
    draw.text((60,y+85),title,fill="white")
    y+=240
p=os.path.expanduser("~/M82/M82_Cards/MORGAN_ARCHITECTURE_9.8.png")
os.makedirs(os.path.dirname(p),exist_ok=True)
img.save(p)
print(f"🟢 [MORGAN CATHEDRAL] {p}")
