import os, re

path = os.path.expanduser("~/M82/orch.py")

with open(path, "r") as f:
    code = f.read()

# 1. Eliminar patrones de prefijo como [BANKING | Caracas HQ], [BANKING], [TREASURY | Caracas HQ], etc.
patch_pattern = r"cleaned = re.sub(r'\[[A-Z_\s\|]+\]', '', cleaned).strip()"

if "re.sub(r'\[[A-Z_\\s\\|]+\]'" not in code:
    code = code.replace(
        "cleaned = raw_text.replace(\"High speed wire update.\", \"\").replace(\"[M82]\", \"\").strip()",
        "cleaned = raw_text.replace(\"High speed wire update.\", \"\").replace(\"[M82]\", \"\").strip()\n    cleaned = re.sub(r'\\[[A-Z_\\s\\|]+\\b.*?\\]', '', cleaned).strip()"
    )

# 2. Ajuste en el formateador de caption para ganar el máximo de caracteres útiles
code = code.replace("🏛 [{lseg['desk']}] ", "🏛 ")

with open(path, "w") as f:
    f.write(code)

print("✅ Parche de supresión de sub-cabeceras aplicado con éxito.")
