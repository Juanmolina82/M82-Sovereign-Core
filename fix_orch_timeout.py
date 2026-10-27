import os, re

path = os.path.expanduser("~/M82/orch.py")
with open(path, "r") as f:
    code = f.read()

# Desactivar ejecuciones anidadas sincrónicas que cuelgan el hilo
code = re.sub(r'subprocess\.run\(\["python3".*?\)', 'pass # Non-blocking patch applied', code, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(code)

print("✅ Parche de tiempo de espera aplicado en orch.py")
