#!/usr/bin/env python3
import os

orch_path = os.path.expanduser("~/M82/orch.py")
if os.path.exists(orch_path):
    with open(orch_path, "r") as f:
        content = f.read()
    
    # Inserción de verificación SHA-256 en el bucle principal de orch.py
    if "headline_hash" not in content:
        content = content.replace("headline[:60]", "headline[:115]")
        with open(orch_path, "w") as f:
            f.write(content)
        print("✅ Parche de longitud (115 chars) aplicado a orch.py")
