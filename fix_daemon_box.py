import os, re

path = os.path.expanduser("~/M82/orch.py")

if os.path.exists(path):
    with open(path, "r") as f:
        code = f.read()

    # Se ajusta la caja de la etiqueta Daemon a cálculo dinámico o recorte seguro (16 chars max)
    old_box = "draw.rectangle([55, 145, 520, 205], fill='#0c182b', outline='#00b0ff', width=2)"
    old_text = "draw.text((70, 162), f\"DAEMON: {clean_src[:20]}\", fill='#ffffff', font=f_tag)"

    new_render_logic = """# 2. Label Daemon Source (Caja Dinámica Auto-ajustada)
    clean_src = str(daemon_source).replace("DAEMON: ", "").strip()
    daemon_label = f"DAEMON: {clean_src[:16]}"
    text_w = draw.textlength(daemon_label, font=f_tag) if hasattr(draw, "textlength") else 400
    box_right = max(520, 80 + int(text_w))
    draw.rectangle([55, 145, box_right, 205], fill='#0c182b', outline='#00b0ff', width=2)
    draw.text((70, 162), daemon_label, fill='#ffffff', font=f_tag)"""

    if old_box in code:
        code = code.replace(old_box + "\n    " + old_text, new_render_logic)
        code = code.replace(old_box + "\n    clean_src = str(daemon_source).replace(\"DAEMON: \", \"\").strip()\n    " + old_text, new_render_logic)

    with open(path, "w") as f:
        f.write(code)

    print("🟢 [M82 SUCCESS] orch.py actualizado con caja de Daemon auto-ajustable.")
else:
    print("⚠️ [M82 WARN] ~/M82/orch.py no encontrado.")

