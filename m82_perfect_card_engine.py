#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sqlite3, os, json, datetime, textwrap

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

def generate_perfect_m82_card(headline_text, output_filename="hud_texas_oil_break.png"):
    # Aspect Ratio 4:5 (1080x1350 px)
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.patch.set_facecolor('#04070d')
    
    ax = fig.add_subplot(111)
    ax.set_facecolor('#04070d')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 1. Red de Constelación sutil en el fondo
    np.random.seed(82)
    x_nodes = np.random.uniform(10, 90, 24)
    y_nodes = np.random.uniform(10, 90, 24)
    
    for i in range(len(x_nodes)):
        for j in range(i + 1, len(x_nodes)):
            dist = np.hypot(x_nodes[i] - x_nodes[j], y_nodes[i] - y_nodes[j])
            if dist < 24:
                ax.plot([x_nodes[i], x_nodes[j]], [y_nodes[i], y_nodes[j]], 
                        color='#162436', alpha=0.35, linewidth=0.8)
    
    ax.scatter(x_nodes, y_nodes, color='#00e5ff', s=12, alpha=0.35)

    # 2. Esquinas cibernéticas (Corner Brackets)
    ax.plot([4, 12], [96, 96], color='#1e2d42', linewidth=2)
    ax.plot([4, 4], [96, 88], color='#1e2d42', linewidth=2)
    ax.plot([88, 96], [96, 96], color='#1e2d42', linewidth=2)
    ax.plot([96, 96], [96, 88], color='#1e2d42', linewidth=2)
    ax.plot([4, 12], [4, 4], color='#1e2d42', linewidth=2)
    ax.plot([4, 4], [4, 14], color='#1e2d42', linewidth=2)
    ax.plot([88, 96], [4, 4], color='#1e2d42', linewidth=2)
    ax.plot([96, 96], [4, 14], color='#1e2d42', linewidth=2)

    # 3. Encabezado de la Tarjeta
    ax.text(7, 92, "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM", 
            color='#3a506b', fontsize=11, fontfamily='sans-serif', fontweight='bold')
    
    ax.text(7, 86, "#M82 BREAKING STREAM", 
            color='#e63946', fontsize=28, fontweight='bold', fontfamily='sans-serif')
    
    ax.plot([7, 93], [82, 82], color='#162436', linewidth=1.2)

    # 4. Formato y Tamaño de Texto idéntico a la plantilla exacta
    wrapped_lines = textwrap.wrap(headline_text, width=24)
    
    # Selección de tamaño grande para presencia ejecutiva
    if len(wrapped_lines) <= 4:
        font_size = 38
        line_spacing = 8.5
    elif len(wrapped_lines) <= 6:
        font_size = 34
        line_spacing = 7.5
    else:
        font_size = 28
        line_spacing = 6.5

    y_text = 72
    for line in wrapped_lines:
        ax.text(7, y_text, line, color='#ffffff', fontsize=font_size, fontweight='normal', 
                fontfamily='sans-serif')
        y_text -= line_spacing

    # 5. Pie de página y Marca de Agua
    ax.plot([7, 93], [18, 18], color='#162436', linewidth=1.2)
    
    ax.text(7, 13, "[ AGI QUANTUM VERIFIED ]", color='#00e5ff', fontsize=11, fontfamily='sans-serif', fontweight='bold')
    
    # Firma en una sola línea
    ax.text(7, 6.5, "@MolinaHoldings ", color='#ffffff', fontsize=26, fontweight='bold', fontfamily='sans-serif')
    ax.text(54, 6.5, "LLC", color='#8c9ba5', fontsize=24, fontweight='bold', fontfamily='sans-serif')

    out_path = os.path.join(BASE_DIR, output_filename)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=100)
    plt.close()
    print(f"✅ Tarjeta M82 generada perfectamente: {out_path}")
    return out_path

# --- Ingesta en Base de Datos ---
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
now = datetime.datetime.now().isoformat()

headline = "Texas oil, gas production increases slightly in third quarter as Iran War uncertainty remains"
daemon_id = "m82_texas_energy_daemon.py"

c.execute("""
    INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'DISPATCHED', ?)
    ON CONFLICT(daemon_source, headline) DO UPDATE SET timestamp=excluded.timestamp
""", (daemon_id, headline, now))

c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
    VALUES (?, 'GLOBAL_MACRO_TEXAS', ?, 98.2, 0.02, 1.15, 9.7, ?)
""", (daemon_id, headline, json.dumps({"status": "PERFECT_CARD_ACTIVE", "card": "hud_texas_oil_break.png"})))

conn.commit()
conn.close()

# Generar la imagen
generate_perfect_m82_card(headline, "hud_texas_oil_break.png")
