import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs(os.path.expanduser("~/M82"), exist_ok=True)
output_path = os.path.expanduser("~/M82/m82_institutional_arch.png")

fig = plt.figure(figsize=(12, 7), facecolor='#070b12')
ax = fig.add_subplot(111)
ax.set_facecolor('#070b12')

# Título del Diagrama
ax.text(0.05, 0.92, "M82 QUANTUM MACRO DOSSIER // INSTITUTIONAL PIPELINE V2", 
        color='#38bdf8', fontsize=14, fontweight='bold', family='monospace')
ax.text(0.05, 0.88, "ZeroMQ Pub/Sub + Asyncio NLP Scorer + SQLite WAL Mode", 
        color='#6b7280', fontsize=10, family='monospace')

# Definición de Cajas de Procesamiento
boxes = [
    {"title": "FEEDS & SOURCES\n(40 Daemons)", "x": 0.05, "y": 0.55, "w": 0.18, "h": 0.2, "color": '#1e293b', "border": '#3b82f6'},
    {"title": "ZEROMQ BUS\n(:5555 PUB/SUB)", "x": 0.28, "y": 0.55, "w": 0.18, "h": 0.2, "color": '#1e293b', "border": '#06b6d4'},
    {"title": "ASYNC NLP ENGINE\n(Score >= 7/10)", "x": 0.51, "y": 0.55, "w": 0.20, "h": 0.2, "color": '#1e293b', "border": '#10b981'},
    {"title": "STORAGE CORE\n(SQLite WAL)", "x": 0.76, "y": 0.55, "w": 0.19, "h": 0.2, "color": '#1e293b', "border": '#f59e0b'},
]

for b in boxes:
    rect = patches.FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"],
                                  boxstyle="round,pad=0.02",
                                  facecolor=b["color"], edgecolor=b["border"], linewidth=2)
    ax.add_patch(rect)
    ax.text(b["x"] + b["w"]/2, b["y"] + b["h"]/2, b["title"],
            color='#ffffff', fontsize=9, fontweight='bold',
            ha='center', va='center', family='monospace')

# Flechas de Conexión
arrow_props = dict(arrowstyle="->", color='#38bdf8', lw=2.5)
ax.annotate('', xy=(0.28, 0.65), xytext=(0.23, 0.65), arrowprops=arrow_props)
ax.annotate('', xy=(0.51, 0.65), xytext=(0.46, 0.65), arrowprops=arrow_props)
ax.annotate('', xy=(0.76, 0.65), xytext=(0.71, 0.65), arrowprops=arrow_props)

# Módulo Inferior: HUD Card Generator con Sparkline Preview
hud_rect = patches.FancyBboxPatch((0.05, 0.10), 0.90, 0.35,
                                  boxstyle="round,pad=0.02",
                                  facecolor='#0f172a', edgecolor='#334155', linewidth=1.5)
ax.add_patch(hud_rect)

ax.text(0.08, 0.38, "HUD DISPLAY CARD OVERLAY (PREVIEW)", 
        color='#94a3b8', fontsize=10, fontweight='bold', family='monospace')
ax.text(0.08, 0.30, "#M82 BREAKING [NABEP / BOJ / PCE SPIKE DETECTED]", 
        color='#ef4444', fontsize=11, fontweight='bold', family='monospace')

# Inserción de Sparkline en la parte inferior del HUD
ax_spark = fig.add_axes([0.08, 0.14, 0.35, 0.12])
ax_spark.set_facecolor('#0f172a')
ax_spark.plot([91.2, 92.0, 91.8, 95.4, 98.1, 103.71], color='#00a2ff', lw=2)
ax_spark.axhline(100, color='#ef4444', linestyle='--', linewidth=0.8)
ax_spark.axis('off')

ax.text(0.46, 0.20, "BRENT: $103.71 (+5.8%)\nUST 10Y: 5.272%\nVIX: 18.20", 
        color='#38bdf8', fontsize=10, family='monospace', va='center')
ax.text(0.46, 0.13, "STATUS: SENT_DISPATCHED -> Telegram / NTFY", 
        color='#10b981', fontsize=9, fontweight='bold', family='monospace')

ax.axis('off')
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#070b12')
print(f"✅ Esquema gráfico generado exitosamente en: {output_path}")
