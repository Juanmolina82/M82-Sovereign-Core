#!/usr/bin/env python3
"""
================================================================================
 M82 MACRO-INTELLIGENCE // HUD CARD GENERATOR (STREAM TEMPLATE)
================================================================================
 Genera tarjetas con el formato visual cibernético de #M82 BREAKING STREAM:
  - Fondo oscuro con red/nodo cuántico superpuesto
  - Marcadores de esquina [┌ ┐ └ ┘]
  - Cabecera: SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms
  - Título rojo: #M82 BREAKING STREAM
  - Texto central dinámico en tipografía Serif/Clean
  - Pie de página: [ AGI QUANTUM VERIFIED ] y @MolinaHoldings LLC
"""

import os
import sqlite3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")
OUTPUT_IMG = os.path.join(BASE_DIR, "m82_breaking_stream_card.png")

def generate_stream_card(headline_text="Trump administration ad paid with U.S. funds sparks bipartisan backlash ahead of midterms", category="#M82 BREAKING STREAM"):
    # Dimensiones y resolución de alta definición
    fig, ax = plt.subplots(figsize=(8, 10), dpi=200)
    fig.patch.set_facecolor('#05070a')
    ax.set_facecolor('#05070a')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 1. Red Cuántica de Nodos (Diagrama de fondo)
    np.random.seed(82)
    n_nodes = 30
    x_nodes = np.random.uniform(5, 95, n_nodes)
    y_nodes = np.random.uniform(10, 90, n_nodes)

    # Dibujar conexiones de baja opacidad
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            dist = np.hypot(x_nodes[i] - x_nodes[j], y_nodes[i] - y_nodes[j])
            if dist < 25:
                alpha = (1 - dist / 25) * 0.18
                ax.plot([x_nodes[i], x_nodes[j]], [y_nodes[i], y_nodes[j]], color='#1e4270', linewidth=0.8, alpha=alpha)

    # Dibujar puntos/nodos
    ax.scatter(x_nodes, y_nodes, color='#00a2ff', s=6, alpha=0.35, zorder=2)

    # 2. Marcadores de Esquina (Encuadre HUD)
    corner_color = '#d0d8e0'
    c_len = 4
    # Top-Left ┌
    ax.plot([4, 4 + c_len], [96, 96], color=corner_color, lw=1.2)
    ax.plot([4, 4], [96, 96 - c_len], color=corner_color, lw=1.2)
    # Top-Right ┐
    ax.plot([96 - c_len, 96], [96, 96], color=corner_color, lw=1.2)
    ax.plot([96, 96], [96, 96 - c_len], color=corner_color, lw=1.2)
    # Bottom-Left └
    ax.plot([4, 4 + c_len], [4, 4], color=corner_color, lw=1.2)
    ax.plot([4, 4], [4, 4 + c_len], color=corner_color, lw=1.2)
    # Bottom-Right ┘
    ax.plot([96 - c_len, 96], [4, 4], color=corner_color, lw=1.2)
    ax.plot([96, 96], [4, 4 + c_len], color=corner_color, lw=1.2)

    # 3. Encabezado Técnico
    ax.text(8, 93, "SYSTEM: AGI-CORE // QUANTUM NODE: M82-STREAM // LATENCY: 0.012ms",
            color='#3a5d85', fontsize=7, fontweight='bold', family='monospace')
    
    # Titular de Categoría Red (#M82 BREAKING STREAM)
    ax.text(8, 88, category, color='#d92b2b', fontsize=18, fontweight='bold', family='sans-serif')
    
    # Línea Divisoria Superior
    ax.plot([8, 92], [85, 85], color='#112233', lw=1)

    # 4. Cuerpo de Texto (Titular Principal con Word Wrap)
    import textwrap
    wrapped_lines = textwrap.wrap(headline_text, width=28)
    y_start = 68
    for line in wrapped_lines:
        ax.text(8, y_start, line, color='#f0f4f8', fontsize=22, fontweight='normal', family='serif')
        y_start -= 7.5

    # 5. Pie de Página y Branding
    ax.plot([8, 92], [18, 18], color='#112233', lw=1)
    ax.text(8, 14, "[ AGI QUANTUM VERIFIED ]", color='#1e5b8a', fontsize=7, fontweight='bold', family='monospace')
    
    # Marca @MolinaHoldings LLC
    ax.text(8, 8, "@MolinaHoldings", color='#ffffff', fontsize=14, fontweight='bold', family='sans-serif')
    ax.text(48, 8, "LLC", color='#667788', fontsize=14, fontweight='normal', family='sans-serif')

    plt.tight_layout()
    plt.savefig(OUTPUT_IMG, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"  ✓ Tarjeta HUD M82 generada en: {OUTPUT_IMG}")

if __name__ == "__main__":
    # Intentar obtener la última noticia guardada en SQLite o usar la del formato por defecto
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT headline, category FROM macro_dosier ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
        if row and row[0]:
            generate_stream_card(row[0], f"#M82 {row[1]}")
        else:
            generate_stream_card()
    except Exception:
        generate_stream_card()
