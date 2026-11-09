import os, re

path = os.path.expanduser("~/M82/orch.py")

with open(path, "r") as f:
    code = f.read()

# Crear nueva funcion generate_hud con renderizado completo de la señal
new_generate_hud = '''def generate_hud(headline, source):
    width, height = 1000, 1250
    img = Image.new('RGB', (width, height), color='#070b12')
    draw = ImageDraw.Draw(img)

    font_meta = get_font(26)
    font_header = get_font(36)
    font_main = get_font(44)
    font_footer = get_font(34)

    # Red de Nodos en Fondo
    random.seed(101)
    nodes = [(random.randint(60, 940), random.randint(180, 1050)) for _ in range(18)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            if math.hypot(x2 - x1, y2 - y1) < 260:
                draw.line([(x1, y1), (x2, y2)], fill='#10233b', width=2)
    for x, y in nodes:
        draw.ellipse([x-5, y-5, x+5, y+5], fill='#38bdf8')

    # Esquinas Ciberpunk
    b_len, b_pad = 45, 30
    draw.line([(b_pad, b_pad), (b_pad + b_len, b_pad)], fill='#ef4444', width=4)
    draw.line([(b_pad, b_pad), (b_pad, b_pad + b_len)], fill='#ef4444', width=4)
    draw.line([(width - b_pad, b_pad), (width - b_pad - b_len, b_pad)], fill='#ef4444', width=4)
    draw.line([(width - b_pad, b_pad), (width - b_pad, b_pad + b_len)], fill='#ef4444', width=4)

    # Cabecera M82
    draw.text((60, 50), "SYSTEM: AGI-CORE // NODE: M82 CHARALLAVE", fill='#38bdf8', font=font_meta)
    draw.text((60, 90), "🚨 #M82 #BREAKING STREAM", fill='#ef4444', font=font_header)
    draw.text((60, 135), f"🔴 [{str(source).upper()}]", fill='#38bdf8', font=font_meta)
    draw.line([(60, 175), (width - 60, 175)], fill='#1f2937', width=3)

    # Contenido Completo del Texto
    display_text = f"{source} :: {headline}" if source and not headline.startswith(str(source)) else headline
    lines = textwrap.wrap(display_text, width=28)
    y_text = 220
    for line in lines[:8]:  # Hasta 8 lineas limpias
        draw.text((60, y_text), line, fill='#ffffff', font=font_main)
        y_text += 60

    # Pie de Tarjeta
    draw.line([(60, height - 140), (width - 60, height - 140)], fill='#1f2937', width=3)
    draw.text((60, height - 105), "[ AGI QUANTUM VERIFIED — 0.30x LOCK ]", fill='#2563eb', font=font_meta)
    draw.text((60, height - 65), "🏛 @MolinaHoldings | AGI Quantum Node", fill='#ffffff', font=font_footer)

    img.save(IMG_PATH)
    
    gallery_file = os.path.join(GALLERY_DIR, f"M82_CARD_{int(time.time())}.png")
    try:
        shutil.copy(IMG_PATH, gallery_file)
        subprocess.run(["termux-media-scan", gallery_file], check=False)
    except Exception:
        pass
        
    return IMG_PATH'''

# Sustituir la funcion en orch.py usando regex
pattern = r"def generate_hud\(headline, source\):.*?return IMG_PATH"
updated_code = re.sub(pattern, new_generate_hud, code, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(updated_code)

print("✅ Generador HUD actualizado exitosamente en orch.py")
