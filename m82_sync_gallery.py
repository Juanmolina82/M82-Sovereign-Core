#!/usr/bin/env python3
import os, sys, shutil, subprocess, time

SOURCE_IMG = os.path.expanduser("~/M82/m82_card.png")
TARGET_DIR = "/sdcard/Pictures/M82_Cards"

def sync_to_gallery():
    if not os.path.exists(SOURCE_IMG):
        print("❌ No se encontró ~/M82/m82_card.png para copiar.")
        return

    os.makedirs(TARGET_DIR, exist_ok=True)
    filename = f"M82_CARD_{int(time.time())}.png"
    target_path = os.path.join(TARGET_DIR, filename)

    # 1. Copiar imagen al almacenamiento público
    shutil.copy(SOURCE_IMG, target_path)

    # 2. Forzar escaneo de medios para que aparezca en la app Galería / Fotos
    subprocess.run(["termux-media-scan", target_path], check=False)
    subprocess.run(["termux-media-scan", TARGET_DIR], check=False)

    print(f"📸 Tarjeta sincronizada a Galería Android: {target_path}")

if __name__ == "__main__":
    sync_to_gallery()
