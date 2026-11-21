#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sqlite3, os, json, datetime, textwrap

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

def generate_ultra_breaking_card(headline_text, tag="VENEZUELA_DESK", output_filename="hud_venezuela_ultra.png"):
    # Target Resolution: 1080x1350 px (4:5 Aspect Ratio)
    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.patch.set_facecolor('#04070d')
    
    ax = fig.add_subplot(111)
    ax.set_facecolor('#04070d')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 1. Red Constelación de Fondo
    np.random.seed(82)
    x_nodes = np.random.uniform(5, 95, 28)
    y_nodes = np.random.uniform(5, 95, 28)
    
    for i in range(len(x_nodes)):
        for j in range(i + 1, len(x_nodes)):
            dist = np.hypot(x_nodes[i] - x_nodes[j], y_nodes[i] - y_nodes[j])
            if dist < 22:
                ax.plot([x_nodes[i], x_nodes[j]], [y_nodes[i], y_nodes[j]], 
                        color='#1e2d42', alpha=0.30, linewidth=0.8)
    
    ax.scatter(x_nodes, y_nodes, color='#00e5ff', s=14, alpha=0.4)

    # 2. Marcos de Esquina (Corner Brackets)
    ax.plot([3, 14], [97, 97], color='#ffffff', linewidth=2.5)
    ax.plot([3, 3], [97, 86], color='#ffffff', linewidth=2.5)
    ax.plot([86, 97], [97, 97], color='#ffffff', linewidth=2.5)
    ax.plot([97, 97], [97, 86], color='#ffffff', linewidth=2.5)
    ax.plot([3, 14], [3, 3], color='#ffffff', linewidth=2.5)
    ax.plot([3, 3], [3, 14], color='#ffffff', linewidth=2.5)
    ax.plot([86, 97], [3, 3], color='#ffffff', linewidth=2.5)
    ax.plot([97, 97], [3, 14], color='#ffffff', linewidth=2.5)

    # 3. Encabezados Principales
    ax.text(6, 93, "SYSTEM: AGI-CORE // QUANTUM NODE M82-STREAM // LATENCY: 0.012ms", 
            color='#5a7394', fontsize=11, fontfamily='monospace', fontweight='bold')
    
    ax.text(6, 86, f"#M82 BREAKING [{tag}]", 
            color='#ff1744', fontsize=28, fontweight='black', fontfamily='sans-serif')
    
    ax.plot([6, 94], [83, 83], color='#1e2d42', linewidth=1.5)

    # 4. CONFIGURACIÓN DE FUENTE ULTRA-GIGANTE (OCUPA TODO EL PANEL CENTRAL)
    # Ancho de envoltorio extendido para aprovechar la tarjeta completa
    wrapped_lines = textwrap.wrap(headline_text, width=26)
    
    # Fuentes ultra-prominentes
    if len(wrapped_lines) <= 3:
        font_size = 46
        line_spacing = 11.5
    elif len(wrapped_lines) <= 5:
        font_size = 38
        line_spacing = 9.8
    else:
        font_size = 32
        line_spacing = 8.2

    # Placa cibernética traslúcida con borde neón
    box_height = len(wrapped_lines) * line_spacing + 8
    rect = plt.Rectangle((5, 77 - box_height), 90, box_height, 
                         facecolor='#060a12', alpha=0.94, edgecolor='#00e5ff', linewidth=1.8, zorder=3)
    ax.add_patch(rect)

    y_text = 71
    for line in wrapped_lines:
        ax.text(7.5, y_text, line, color='#ffffff', fontsize=font_size, fontweight='black', 
                fontfamily='sans-serif', zorder=4)
        y_text -= line_spacing

    # 5. WATERMARK UNIFICADO
    ax.text(6, 11, "[ AGI QUANTUM VERIFIED ]", color='#00e5ff', fontsize=12, fontfamily='monospace', fontweight='bold')
    ax.text(6, 5.5, "@MolinaHoldings LLC", color='#ffffff', fontsize=28, fontweight='black', fontfamily='sans-serif')

    out_path = os.path.join(BASE_DIR, output_filename)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=100)
    plt.close()
    print(f"✅ Tarjeta Ultra-Text generada exitosamente: {out_path}")
    return out_path

# Ingesta en Base de Datos
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
now = datetime.datetime.now().isoformat()

headline = "Exclusive | Pentagon-Backed Oil Company Is Set to Vie for Chevron’s Crown in Venezuela"
daemon_id = "m82_machado_delcy_cable_daemon.py"

c.execute("""
    INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp)
    VALUES (?, ?, 'DISPATCHED', ?)
    ON CONFLICT(daemon_source, headline) DO UPDATE SET timestamp=excluded.timestamp
""", (daemon_id, headline, now))

c.execute("""
    INSERT INTO macro_dosier (source, category, headline, gprk_index, yield_10y_delta, oil_spread_impact, risk_score, metadata_json)
    VALUES (?, 'VENEZUELA_PENTAGON_OIL', ?, 99.4, 0.03, 1.45, 9.9, ?)
""", (daemon_id, headline, json.dumps({"status": "ULTRA_CARD_ACTIVE", "card": "hud_venezuela_ultra.png"})))

conn.commit()
conn.close()

# Generación del gráfico
generate_ultra_breaking_card(headline, "VENEZUELA_DESK", "hud_venezuela_ultra.png")
