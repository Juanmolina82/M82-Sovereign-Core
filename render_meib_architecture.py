#!/usr/bin/env python3
# ==============================================================================
# M82 BLUEPRINT RENDER ENGINE -- MEIB ARCHITECTURE v61.0.1 (CORNICHE PITCH)
# Chairman Juan M. Molina -- Sede Operativa Nodo Charallave L4/L5 Edge
# ==============================================================================
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.expanduser("~/M82/certs_v61")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "MEIB_Architecture_v61.0.1_Caracas.png")

def get_font(size):
    for font_path in [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/Roboto-Regular.ttf",
        "/system/fonts/DroidSans-Bold.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
    ]:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def render_meib_card():
    W, H = 1080, 1350
    img = Image.new('RGB', (W, H), color='#04070d')
    draw = ImageDraw.Draw(img)

    f_title = get_font(30)
    f_sub = get_font(20)
    f_sec = get_font(24)
    f_body = get_font(20)
    f_bold = get_font(22)
    f_ftr = get_font(18)

    # Marco Perimetral
    draw.rectangle([20, 20, W - 20, H - 20], outline='#ffb300', width=4)
    draw.rectangle([35, 35, W - 35, 140], fill='#0a111f', outline='#1a2a45', width=2)

    # Header Institucional
    draw.text((50, 48), "MOLINA ENERGY INVESTMENT BANKING (MEIB)", fill='#ffb300', font=f_title)
    draw.text((50, 95), "CROSS-BORDER PLATFORM :: NASHVILLE, TN ⊗ CARACAS, VZ (JMM C.A.)", fill='#00e5ff', font=f_sub)

    # Bloque 1: Matriz de 3 Capas
    draw.rectangle([50, 160, W - 50, 520], fill='#070d18', outline='#122038', width=2)
    draw.text((70, 180), "🏛️ ARCHITECTURE LAYER STACK (3-CAPAS SOBERANAS)", fill='#ffb300', font=f_sec)
    draw.line([(70, 215), (W - 70, 215)], fill='#ffb300', width=2)

    l1 = "CAPA 1 :: 188Y MORGAN DYNASTY TRUST (1837-2025) -- Legacy Kidder Peabody & NationsBank"
    l2 = "CAPA 2 :: MEIB CROSS-BORDER PLATFORM -- Private Credit, Mezzanine, Quad-SPV Ring-Fenced"
    l3 = "CAPA 3 :: 0.10x GAS-TO-COMPUTE OFF-GRID -- Caracas/Charallave Edge (GE Vernova $340 USD)"
    
    draw.text((70, 235), l1, fill='#ffffff', font=f_bold)
    draw.text((70, 295), l2, fill='#ffffff', font=f_bold)
    draw.text((70, 355), l3, fill='#ffffff', font=f_bold)

    draw.text((70, 420), "• Hub USA: Nashville, TN (GP/LP Syndication, Infra Funds & Institutional LPs)", fill='#00e5ff', font=f_body)
    draw.text((70, 460), "• Hub VZ: Caracas HQ / Corp Int JMM C.A. (Exp 220-54602 - 91% Superquórum)", fill='#00e5ff', font=f_body)

    # Bloque 2: Indicadores & M&A Mandates
    draw.rectangle([50, 540, W - 50, 960], fill='#070d18', outline='#122038', width=2)
    draw.text((70, 560), "💼 CORNICHE PITCH MUNITION & MANDATE SCOPE", fill='#ff3d00', font=f_sec)
    draw.line([(70, 595), (W - 70, 595)], fill='#ff3d00', width=2)

    lines = [
        "• Private Equity & Private Credit: Unitranche, Preferred Equity & Mezzanine Financing.",
        "• Hard-Asset Backed Credit: Long-term Offtake Contracts & Caribbean Storage Infrastructure.",
        "• Midstream & Terminals: Oil & Gas, Dry-Bulk Vessels (Aframax/Suezmax/VLCC) & Logistics.",
        "• AI Hedging Engine: Strategic Energy, Gold & CO2 Portfolio Risk Management (#M82 & #C02).",
        "• Arbitrage Asymmetry: 0.10x Energy/Eng. Cost in VZ vs. US $64B/qtr Squeeze (FCF -$9B)."
    ]
    y_pos = 620
    for line in lines:
        draw.text((70, y_pos), line, fill='#e0e0e0', font=f_body)
        y_pos += 65

    # Bloque 3: M82 Sovereign Core Metrics
    draw.rectangle([50, 980, W - 50, 1200], fill='#0a1424', outline='#00b0ff', width=2)
    draw.text((70, 1000), "🔒 M82 SOVEREIGN CORE METRICS & GOVERNANCE", fill='#00e5ff', font=f_sec)
    draw.text((70, 1050), "• Sovereign Index (MSI): 1500.0 PTS (150x Benchmark US Model <10.0)", fill='#ffffff', font=f_bold)
    draw.text((70, 1090), "• Power Equation: Base Indestructible 444 = $4.444T USD = Trust > Money", fill='#ffb300', font=f_bold)
    draw.text((70, 1130), "• Risk Status: BUNKER MODE 0.30x LOCK | VaR: 1.68% | WAL Clean 0/0/0 (43/43)", fill='#00e5ff', font=f_body)

    # Footer
    draw.rectangle([35, 1220, W - 35, 1315], fill='#0a111f', outline='#1a2a45', width=2)
    draw.text((50, 1240), "CERTIFICATE NO: SCV61-1500-M82-444-TRUST | RELEASE: v61.0.1 PERPETUAL", fill='#ffb300', font=f_ftr)
    draw.text((50, 1275), "EXECUTIVE AUTHORITY: CHAIRMAN JUAN M. MOLINA | MOLINA HOLDINGS LLC", fill='#ffffff', font=f_ftr)

    img.save(OUTPUT_FILE)
    os.system(f"termux-media-scan '{OUTPUT_FILE}' >/dev/null 2>&1 || true")
    print(f"🟢 [RENDER SUCCESS] Blueprint visual generado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    render_meib_card()
