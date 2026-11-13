#!/usr/bin/env python3
# M82 PRIVATE LOCAL - Disparo a privado del Chairman
# Mesa de Dinero + Contexto Economico Global
import os, json, time, datetime

BASE = os.path.expanduser("~/M82/private")
os.makedirs(f"{BASE}/resumenes", exist_ok=True)
LOG = f"{BASE}/resumenes/resumen_m82_privado.md"

def disparar(titulo, mesa, global_ctx, decision):
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")
    bloque = f"""
---
## {titulo}
**Fecha:** {ahora}
**Chairman:** Juan M. Molina - jmmp@molina82.com
**Rama:** main - BUNKER 0.30x LOCK - 100% Dry Powder

### MESA DE DINERO
{mesa}

### CONTEXTO ECONOMICO GLOBAL
{global_ctx}

### DECISION SELLADA
{decision}

**Fable construye. Mythos audita. Caracas manda. Charallave ejecuta.**
"""
    with open(LOG, "a") as f:
        f.write(bloque)
    print(f"[PRIVATE LOCAL OK] Guardado en {LOG}")
    print(bloque)

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 5:
        disparar(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Uso: python3 m82_private_local.py 'Titulo' 'Mesa' 'Global' 'Decision'")
