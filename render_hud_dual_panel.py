#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

BASE_DIR = os.path.expanduser("~/M82")

plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=200)
fig.patch.set_facecolor('#0a0d12')

# Panel 1: Curva de Rendimientos (2Y vs 10Y vs 30Y)
tenors = ['2Y Yield', '10Y Yield', '30Y Yield']
rates = [4.868, 5.272, 5.6298]
colors = ['#00e5ff', '#ff1744', '#ffea00']

bars1 = ax1.bar(tenors, rates, color=colors, edgecolor='#76ff03', alpha=0.85, width=0.5)
ax1.set_facecolor('#0f141d')
ax1.set_ylabel('Rendimiento (%)', fontsize=9, fontweight='bold', color='#00e5ff')
ax1.set_title('US TREASURY DIVERGENCE (2Y 4.868% vs 10Y 5.272%)', fontsize=10, fontweight='bold', color='#76ff03')
ax1.set_ylim(4.0, 6.0)
ax1.grid(True, linestyle='--', alpha=0.2, color='#00e5ff')

for bar in bars1:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h + 0.04, f'{h:.3f}%', ha='center', va='bottom', fontsize=8, fontweight='bold', color='#ffffff')

# Panel 2: Energy Spreads (WTI vs Brent $103.71)
crude_types = ['WTI Crude', 'Brent Crude']
prices = [91.33, 103.71]
c_colors = ['#ff9100', '#d50000']

bars2 = ax2.bar(crude_types, prices, color=c_colors, edgecolor='#76ff03', alpha=0.85, width=0.4)
ax2.set_facecolor('#0f141d')
ax2.set_ylabel('Precio USD / Bbl', fontsize=9, fontweight='bold', color='#00e5ff')
ax2.set_title('ENERGY SPREADS & FAJA IMPACT ($103.71)', fontsize=10, fontweight='bold', color='#76ff03')
ax2.set_ylim(80.0, 115.0)
ax2.grid(True, linestyle='--', alpha=0.2, color='#00e5ff')

for bar in bars2:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, h + 1.0, f'${h:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color='#ffffff')

plt.suptitle('M82 MACRO DOSIER // M82_MACRO REUTERS WIRE DUAL-PANEL TELEMETRY', fontsize=12, fontweight='bold', color='#00e5ff', y=0.98)
plt.tight_layout()

hud_dual_path = os.path.join(BASE_DIR, "hud_m82_macro_wire_dual_panel.png")
plt.savefig(hud_dual_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

print(f"✅ HUD Dual-Panel 'hud_m82_macro_wire_dual_panel.png' generado exitosamente en ~/M82.")
