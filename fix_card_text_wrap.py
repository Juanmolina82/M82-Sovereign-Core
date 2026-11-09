import os, re

path = os.path.expanduser("~/M82/orch.py")

with open(path, "r") as f:
    code = f.read()

# 1. Ajustar el tamaño de fuente para el cuerpo principal
code = code.replace("font_main = get_font(42)", "font_main = get_font(32)")

# 2. Reducir el ancho de envoltorio de 30 a 22 caracteres
code = code.replace("lines = textwrap.wrap(parsed['headline'], width=30)", "lines = textwrap.wrap(parsed['headline'], width=22)")

# 3. Ajustar el interlineado y limitar a 7 líneas para no colisionar con el footer
code = code.replace("y_text += 60", "y_text += 48")
code = code.replace("for line in lines[:10]:", "for line in lines[:7]:")

with open(path, "w") as f:
    f.write(code)

print("✅ Ajuste de tipografía y envoltorio aplicado en orch.py")
