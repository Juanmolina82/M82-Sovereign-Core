import re

file_path = "/data/data/com.termux/files/home/M82/orch.py"
with open(file_path, "r") as f:
    code = f.read()

# Forzar el guardado explícito con ruta de string limpia para Pillow
fixed_code = re.sub(
    r"(\w+)\.save\(([\w_]+),\s*format=([^\)]+)\)",
    r"with open(str(\2), 'wb') as f_out: \1.save(f_out)",
    code
)

with open(file_path, "w") as f:
    f.write(code)

print("HOTFIX APLICADO EN orch.py")
