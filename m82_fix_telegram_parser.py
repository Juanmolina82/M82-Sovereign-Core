#!/usr/bin/env python3
import os, re

files_to_patch = ["orch.py", "m82_dossier_mcm.py", "m82_bot_replicator.py"]

print("⚡ [M82 TG PARSER FIX] Sanitizando parse_mode en scripts telemétricos...")

for fname in files_to_patch:
    fpath = os.path.expanduser(f"~/M82/{fname}")
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()
        
        # Eliminar o sanitizar parse_mode para evitar rebotes HTTP 400 por Markdown/HTML
        patched_content = re.sub(r'["\']parse_mode["\']\s*:\s*["\'].*?["\']', '"parse_mode": "HTML"', content)
        patched_content = re.sub(r'parse_mode\s*=\s*["\'].*?["\']', 'parse_mode="HTML"', patched_content)
        
        with open(fpath, "w", encoding="utf-8") as fp:
            fp.write(patched_content)
        print(f"✅ {fname} sanitizado con éxito.")

print("🚀 Reiniciando orquestador para re-transmisión...")
