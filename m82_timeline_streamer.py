#!/usr/bin/env python3
import os, sys, time, subprocess

M82_DIR = os.path.expanduser("~/M82")
GEN_SCRIPT = os.path.join(M82_DIR, "m82_timeline_generator.py")
SEND_SCRIPT = os.path.join(M82_DIR, "send_timeline.py")

print("🚀 [M82 TIMELINE STREAMER] Iniciando bucle continuo de Refinitiv Workspace Wire...")

while True:
    try:
        # 1. Generar la imagen mas reciente de la linea de tiempo desde Refinitiv
        print("\n🔄 [1/2] Renderizando Timeline HD desde LSEG RDP...")
        subprocess.run(["python3", GEN_SCRIPT], check=True)

        # 2. Despachar a Telegram usando el bot activo
        print("📡 [2/2] Despachando a canal privado Telegram...")
        subprocess.run(["python3", SEND_SCRIPT], check=True)

    except Exception as e:
        print(f"⚠️ Error en ciclo de Timeline Streamer: {e}")

    # Esperar 3 minutos antes de la siguiente actualizacion
    time.sleep(180)
