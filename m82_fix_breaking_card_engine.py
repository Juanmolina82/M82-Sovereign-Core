#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sqlite3, os, json, datetime, textwrap

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

def generate_quantum_breaking_card(headline_text, tag="GLOBAL_MACRO", output_filename="hud_global_macro_break.png"):
    # Resolution: 1080x1350 px (4:5 Ratio)
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.patch.set_facecolor('#04070d')
    
    ax = fig.add_subplot(111)
    ax.set_facecolor('#04070d')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 1. Background Constellation Graph
    np.random.seed(99)
    x_nodes = np.random.uniform(10, 90, 32)
    y_nodes = np.random.uniform(10, 90, 32)
    
    for i in range(len(x_nodes)):
        for j in range(i + 1, len(x_nodes)):
            dist = np.hypot(x_nodes[i] - x_nodes[j], y_nodes[i] - y_nodes[j])
            if dist < 22:
                ax.plot([x_nodes[i], x_nodes[j]], [y_nodes[i], y_nodes[j]], 
                        color='#1a293d', alpha=0.4, linewidth=0.8)
    
    ax.scatter(x_nodes, y_nodes, color='#00e5ff', s=14, alpha=0.6)

    # 2. Precision Corner Brackets
    # Top-Left
    ax.plot([4, 12], [96, 96], color='#ffffff', linewidth=2)
    ax.plot([4, 4], [96, 88], color='#ffffff', linewidth=2)
    # Top-Right
    ax.plot([88, 96], [96, 96], color='#ffffff', linewidth=2)
    ax.plot([96, 96], [96, 88], color='#ffffff', linewidth=2)
    # Bottom-Left
    ax.plot([4, 12], [4, 4], color='#ffffff', linewidth=2)
    ax.plot([4, 4], [4, 12], color='#ffffff', linewidth=2)
    # Bottom-Right
    ax.plot([88, 96], [4, 4], color='#ffffff', linewidth=2)
    ax.plot([96, 96], [4, 12], color='#ffffff', linewidth=2)

    # 3. Header Info
    ax.text(8, 92, "SYSTEM: AGI-CORE // QUANTUM NODE M82-STREAM // LATENCY: 0.012ms", 
            color='#425875', fontsize=10, fontfamily='monospace', fontweight='bold')
    
    ax.text(8, 86, f"#M82 BREAKING [{tag}]", 
            color='#ff1744', fontsize=24, fontweight='black', fontfamily='sans-serif')
    
    ax.plot([8, 92], [84, 84], color='#1e2d42', linewidth=1)

    # 4. Corrected Text Wrapper & Dynamic Scaling (Fixes Text Breaks)
    # Adjust wrapper width dynamically based on text length
    if len(headline_text) > 80:
        wrap_width = 38
        font_size = 22
        line_spacing = 5.2
    else:
        wrap_width = 32
        font_size = 26
        line_spacing = 6.2

    wrapped_lines = textwrap.wrap(headline_text, width=wrap_width)

    # Backdrop HUD Plate for Legibility
    box_height = len(wrapped_lines) * line_spacing + 8
    rect = plt.Rectangle((6, 72 - box_height), 88, box_height, 
                         facecolor='#080e18', alpha=0.88, edgecolor='#00e5ff', linewidth=1.2, zorder=3)
    ax.add_patch(rect)

    y_text = 68
    for line in wrapped_lines:
        ax.text(9, y_text, f'"{line}"' if line == wrapped_lines[0] and len(wrapped_lines) == 1 else line, 
                color='#ffffff', fontsize=font_size, fontweight='bold', fontfamily='serif', zorder=4)
        y_text -= line_spacing

    # 5. Fixed Single-Line Watermark Alignment
    ax.text(8, 12, "[ AGI QUANTUM VERIFIED ]", color='#00e5ff', fontsize=11, fontfamily='monospace', fontweight='bold')
    
    # Combined single call prevents "LLC" displacement
    ax.text(8, 6.5, "@MolinaHoldings ", color='#ffffff', fontsize=24, fontweight='black', fontfamily='sans-serif', display='data')
    ax.text(49, 6.5, "LLC", color='#809ab8', fontsize=22, fontweight='bold', fontfamily='sans-serif', display='data')

    # Output
    out_path = os.path.join(BASE_DIR, output_filename)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=100)
    plt.close()
    print(f"✅ Tarjeta corregida sin saltos ni alineaciones rotas: {out_path}")
    return out_path

# --- Ingesta de la Señal del Wire ---
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
now = datetime.datetime.now().isoformat()

headline = "Oil and gas activity increases despite cost pressures, longer supplier delivery times"
daemon_id = "m82_crypto_commodities_daemon.py"

c.execute("""
    INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'DISPATCHED', ?)
    ON CONFLICT(daemon_source, headline) DO UPDATE SET timestamp=excluded.timestamp
""", (daemon_id, headline, now))

c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
    VALUES (?, 'GLOBAL_MACRO_ENERGY', ?, 97.4, 0.015, 1.08, 9.6, ?)
""", (daemon_id, headline, json.dumps({"status": "CARD_FIXED", "card": "hud_global_macro_break.png"})))

conn.commit()
conn.close()

# Generar la imagen corregida
generate_quantum_breaking_card(headline, "GLOBAL_MACRO", "hud_global_macro_break.png")
