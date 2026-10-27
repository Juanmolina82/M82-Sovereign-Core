import os, re

path = os.path.expanduser("~/M82/orch.py")

with open(path, "r") as f:
    code = f.read()

institutional_hud = '''def generate_hud(headline, source):
    width, height = 1000, 1250
    # Fondo Azul Cobalto Oscuro (Goldman / Terminal)
    img = Image.new('RGB', (width, height), color='#0b0f19')
    draw = ImageDraw.Draw(img)

    font_meta = get_font(24)
    font_sub = get_font(28)
    font_header = get_font(36)
    font_main = get_font(46)
    font_kpi = get_font(26)
    font_footer = get_font(32)

    # Marcadores de Borde Institucionales (Minimalist Bracket)
    draw.rectangle([25, 25, width - 25, height - 25], outline='#1e293b', width=2)
    draw.rectangle([35, 35, width - 35, height - 35], outline='#334155', width=1)

    # Cabecera Terminal
    draw.rectangle([35, 35, width - 35, 110], fill='#0f172a')
    draw.text((60, 50), "M82 SOVEREIGN MONITOR // QUANTUM TERMINAL", fill='#38bdf8', font=font_meta)
    draw.text((60, 78), "SYSTEM: AGI CORE L4/L5 — CHARALLAVE EDGE", fill='#94a3b8', font=font_meta)

    # Linea divisoria Dorada/Azul
    draw.line([(35, 110), (width - 35, 110)], fill='#0284c7', width=3)

    # Ticker / Categoria Tag
    src_clean = str(source).replace('[', '').replace(']', '').upper()
    draw.rectangle([60, 140, 60 + len(src_clean)*22 + 40, 185], fill='#1e293b', outline='#0284c7', width=1)
    draw.text((80, 148), src_clean, fill='#f8fafc', font=font_sub)

    # KPI Matrix Bar (Estilo Citadel HUD)
    draw.rectangle([60, 210, width - 60, 290], fill='#020617', outline='#1e293b', width=1)
    draw.text((80, 225), "EXPOSURE: 0.22x / 0.30x LOCK  |  VaR: 1.68%", fill='#38bdf8', font=font_kpi)
    draw.text((80, 255), "EQUITY: JPM $273.20  |  XLK $190.15  |  WARSH: +102bps", fill='#f59e0b', font=font_kpi)

    # Area Central: Wire Content
    clean_hl = str(headline)
    if clean_hl.startswith(f"[{source}]"):
        clean_hl = clean_hl.replace(f"[{source}]", "").strip()

    lines = textwrap.wrap(clean_hl, width=28)
    y_text = 340

    draw.text((60, y_text), "⚡ BREAKING WIRE TELEMETRY", fill='#ef4444', font=font_header)
    y_text += 60
    draw.line([(60, y_text), (width - 60, y_text)], fill='#1e293b', width=2)
    y_text += 40

    for line in lines[:8]:
        draw.text((60, y_text), line, fill='#ffffff', font=font_main)
        y_text += 65

    # Footer Institucional
    draw.rectangle([35, height - 120, width - 35, height - 35], fill='#0f172a')
    draw.line([(35, height - 120), (width - 35, height - 120)], fill='#0284c7', width=2)

    draw.text((60, height - 100), "[ AGI QUANTUM VERIFIED — CUSTODIA PASIVA 0.30x LOCK ]", fill='#38bdf8', font=font_meta)
    draw.text((60, height - 65), "🏛 @MolinaHoldings | Sovereign Execution Node", fill='#f8fafc', font=font_footer)

    img.save(IMG_PATH)

    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{int(time.time())}.png")
    try:
        shutil.copy(IMG_PATH, gallery_file)
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass

    return IMG_PATH'''

pattern = r"def generate_hud\(headline, source\):.*?return IMG_PATH"
updated_code = re.sub(pattern, institutional_hud, code, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(updated_code)

print("✅ Generador estilo Citadel / Goldman instalado en orch.py")
