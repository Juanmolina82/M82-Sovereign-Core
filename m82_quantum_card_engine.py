#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sqlite3, os, json, datetime

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

def generate_breaking_card(headline_text, category_tag="TRUMP_NEWSROOM", output_filename="hud_trump_tariffs.png"):
    # Target Resolution: 1080x1350 px (Aspect Ratio 4:5 optimized for HUD/PWA Cards)
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.patch.set_facecolor('#04070d') # Deep Space Background
    
    ax = fig.add_subplot(111)
    ax.set_facecolor('#04070d')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 1. Background Constellation Network Effect
    np.random.seed(82)
    x_nodes = np.random.uniform(5, 95, 28)
    y_nodes = np.random.uniform(5, 95, 28)
    
    for i in range(len(x_nodes)):
        for j in range(i + 1, len(x_nodes)):
            dist = np.hypot(x_nodes[i] - x_nodes[j], y_nodes[i] - y_nodes[j])
            if dist < 25:
                ax.plot([x_nodes[i], x_nodes[j]], [y_nodes[i], y_nodes[j]], 
                        color='#1e2d42', alpha=0.35, linewidth=0.8)
    
    ax.scatter(x_nodes, y_nodes, color='#00e5ff', s=12, alpha=0.5)

    # 2. Framing Corner Brackets
    # Top-Left Bracket
    ax.plot([5, 12], [95, 95], color='#ffffff', linewidth=2)
    ax.plot([5, 5], [95, 88], color='#ffffff', linewidth=2)
    # Top-Right Bracket
    ax.plot([88, 95], [95, 95], color='#ffffff', linewidth=2)
    ax.plot([95, 95], [95, 88], color='#ffffff', linewidth=2)
    # Bottom-Left Bracket
    ax.plot([5, 12], [5, 5], color='#ffffff', linewidth=2)
    ax.plot([5, 5], [5, 12], color='#ffffff', linewidth=2)
    # Bottom-Right Bracket
    ax.plot([88, 95], [5, 5], color='#ffffff', linewidth=2)
    ax.plot([95, 95], [5, 12], color='#ffffff', linewidth=2)

    # 3. System Tech Header
    ax.text(8, 91, "SYSTEM: AGI-CORE // QUANTUM NODE M82-STREAM // LATENCY: 0.012ms", 
            color='#425875', fontsize=11, fontfamily='monospace', fontweight='bold')
    
    # 4. Main Title Header
    ax.text(8, 86, "#M82 BREAKING STREAM", 
            color='#ff1744', fontsize=28, fontweight='black', fontfamily='sans-serif')
    
    ax.plot([8, 92], [84, 84], color='#1e2d42', linewidth=1)

    # 5. Core Headline Render (Auto-wrapping text)
    import textwrap
    wrapped_lines = textwrap.wrap(headline_text, width=28)
    
    y_text = 68
    for line in wrapped_lines:
        ax.text(8, y_text, line, color='#ffffff', fontsize=32, fontweight='bold', fontfamily='serif')
        y_text -= 7.5

    # 6. Quantum Verification Footer & Watermark
    ax.text(8, 12, "[ AGI QUANTUM VERIFIED ]", color='#00e5ff', fontsize=12, fontfamily='monospace', fontweight='bold')
    
    ax.text(8, 7, "@MolinaHoldings", color='#ffffff', fontsize=26, fontweight='black', fontfamily='sans-serif')
    ax.text(54, 7, "LLC", color='#809ab8', fontsize=24, fontweight='bold', fontfamily='sans-serif')

    # Output Saving
    out_path = os.path.join(BASE_DIR, output_filename)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=100)
    plt.close()
    print(f"✅ Tarjeta Quantum Full-Size generada: {out_path}")
    return out_path

# --- Ingesta y Anti-Duplicado para la Red de 40 Daemons ---
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
now = datetime.datetime.now().isoformat()

headline = "Trump’s tariffs are back in court — again"
daemon_id = "m82_us_china_tariffs_daemon.py"

# Búsqueda/Insersión controlada contra duplicación
c.execute("""
    INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'DISPATCHED', ?)
    ON CONFLICT(daemon_source, headline) DO UPDATE SET timestamp=excluded.timestamp
""", (daemon_id, headline, now))

c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
    VALUES (?, 'TRUMP_TARIFFS_LEGAL', ?, 98.9, 0.02, 0.95, 9.8, ?)
""", (daemon_id, headline, json.dumps({"court_action": "TARIFF_APPEAL", "card": "hud_trump_tariffs.png"})))

conn.commit()
conn.close()

# Generar la imagen idéntica al diseño pedido
generate_breaking_card(headline, "TRUMP_NEWSROOM", "hud_trump_tariffs.png")
