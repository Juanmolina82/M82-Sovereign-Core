#!/usr/bin/env python3
import shutil
from pathlib import Path

GW_MOBILE = Path.home() / "M82" / "orchestrator" / "m82_mobile_gateway.py"
txt = GW_MOBILE.read_text(encoding="utf-8", errors="ignore")
lines = txt.splitlines()

print("=== CONTEXTO LINEAS 75-105 DE m82_mobile_gateway.py ===")
for idx in range(74, min(len(lines), 105)):
    print(f"L{idx+1}: {lines[idx]}")

# Si existe un respaldo previo valido, restaurarlo; si no, reparar triple comilla abierta en L84
baks = sorted(GW_MOBILE.parent.glob("m82_mobile_gateway.py*bak*"))
restored = False
for b in baks:
    try:
        compile(b.read_text(encoding="utf-8", errors="ignore"), str(b), "exec")
        shutil.copy2(b, GW_MOBILE)
        print(f"[+] Restaurado desde respaldo valido: {b.name}")
        restored = True
        break
    except SyntaxError:
        pass

if not restored:
    shutil.copy2(GW_MOBILE, str(GW_MOBILE) + ".broken_l84")
    # Buscar inicio de re.sub(r''' en L84 y cerrar comillas si quedaron abiertas
    fixed_lines = []
    in_unterminated = False
    for i, l in enumerate(lines, 1):
        if i == 84 and "r'''" in l and l.count("'''") == 1:
            in_unterminated = True
            fixed_lines.append(l)
            continue
        if in_unterminated and (l.strip().startswith("def ") or l.strip().startswith("class ") or l.strip().startswith("if __name__")):
            fixed_lines.append("''', '', src)")
            in_unterminated = False
        fixed_lines.append(l)
    if in_unterminated:
        fixed_lines.append("''', '', src)")
    candidate = "\n".join(fixed_lines) + "\n"
    try:
        compile(candidate, str(GW_MOBILE), "exec")
        GW_MOBILE.write_text(candidate, encoding="utf-8")
        print("[+] Sintaxis de m82_mobile_gateway.py reparada y compilada OK")
    except SyntaxError as e:
        print(f"[!] Error residual en compilacion: {e}")
