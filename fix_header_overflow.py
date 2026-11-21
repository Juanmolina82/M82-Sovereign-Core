import os, re

path = os.path.expanduser("~/M82/orch.py")

with open(path, "r") as f:
    code = f.read()

# 1. Reducir la fuente de la etiqueta Intelligence Layer de 24pt/22pt a 18pt
code = re.sub(
    r"font_intel\s*=\s*get_font\(\d+\)", 
    "font_intel = get_font(18)", 
    code
)

# 2. Alternativa: Reemplazar el texto largo si está hardcodeado para que calce perfecto
code = code.replace(
    "OLLAMA LOCAL (ZERO-CLOUD)", 
    "OLLAMA LOCAL [ZERO-CLOUD]"
)

# 3. Asegurar ajuste dinámico o recorte de padding si dibuja el rectángulo
with open(path, "w") as f:
    f.write(code)

print("✅ Parche de caja superior aplicado en orch.py")
