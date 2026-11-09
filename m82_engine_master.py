#!/usr/bin/env python3
import sqlite3, os, datetime, json
import matplotlib
matplotlib.use('Agg')  # Backend para entornos Headless / Termux
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

def get_db():
    return sqlite3.connect(DB_PATH)

def generate_hud_card(headline, source):
    """Genera una tarjeta gráfica HUD M82 Cyberpunk y retorna su ruta"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=200)
    fig.patch.set_facecolor('#0a0d12')
    ax.set_facecolor('#0f141d')

    funds = [
        'GA Partners IV', 'KKR NA XIV', 'Francisco P. VIII', 
        'Sequoia Cap Fund', 'KKR Global Infra V', 'Coller Int IX', 
        'BPEA PE IX', 'Warburg Pincus 15', 'Veritas Cap IX', 'Clearlake Cap VIII'
    ]
    sizes = [23.70, 23.00, 23.00, 22.72, 19.20, 17.00, 15.60, 15.52, 15.30, 14.80]
    y_pos = np.arange(len(funds))

    bars = ax.barh(y_pos, sizes, align='center', color='#00e5ff', edgecolor='#76ff03', alpha=0.85, height=0.65)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(funds, fontsize=9, fontweight='bold', color='#e0e0e0')
    ax.invert_yaxis()
    ax.set_xlabel('Tamaño del Fondo ($B USD)', fontsize=10, fontweight='bold', color='#00e5ff')
    ax.set_title(f'M82 MACRO DOSIER // {source}\n{headline[:55]}...', fontsize=11, fontweight='bold', color='#76ff03', pad=12)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, f'${width:.2f}B',
                va='center', ha='left', fontsize=8, fontweight='bold', color='#ffffff')

    ax.set_xlim(0, 28)
    ax.grid(True, linestyle='--', alpha=0.2, color='#00e5ff')
    plt.axvline(x=20, color='#ff1744', linestyle=':', linewidth=1.5, label='Threshold Megafondo ($20B)')
    ax.legend(loc='lower right', facecolor='#0a0d12', edgecolor='#76ff03', fontsize=8)

    plt.tight_layout()
    output_path = os.path.join(BASE_DIR, f"hud_{source}.png")
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return output_path

if __name__ == "__main__":
    card = generate_hud_card("Top 10 Largest PE Funds Concentration", "PE_LARGEST_FUNDS_DESK")
    print(f"✅ HUD Render Engine blindado: {card}")
