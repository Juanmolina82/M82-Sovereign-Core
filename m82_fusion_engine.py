#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import requests
import time

def ejecutar_monolito_hibrido():
    # 1. Ejecución nativa ultra rápida del binario de C++
    try:
        resultado_cpp = subprocess.check_output(["./m82_core"], text=True)
    except Exception as e:
        resultado_cpp = f"Fallo en núcleo binario: {str(e)}"

    # 2. Recuperar la API key de Gemini desde el entorno
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        return "❌ ERROR: Variable GEMINI_API_KEY no configurada en Termux."

    # 3. Interfaz de Red REST - Optimizado para Máxima Velocidad (512 tokens budget)
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    
    prompt_tactico = (
        f"Analiza este diagnóstico de nuestro módulo C++:\n'{resultado_cpp}'\n\n"
        "Cruza esto con una búsqueda rápida en internet en tiempo real sobre:\n"
        "1. Estado de última hora de la apertura del Estrecho de Ormuz.\n"
        "2. Precio actual del S&P 500 y Nasdaq de este instante.\n"
        "Genera un informe ultra-condensado, ejecutivo y directo al grano con viñetas y emojis."
    )
    
    gemini_payload = {
        "contents": [{"parts": [{"text": prompt_tactico}]}],
        "tools": [{"googleSearch": {}}],
        "generationConfig": {
            "thinkingConfig": {
                "thinkingBudget": 512  # Velocidad de respuesta optimizada
            }
        }
    }
    
    try:
        response = requests.post(gemini_url, json=gemini_payload, headers={"Content-Type": "application/json"}, timeout=30)
        if response.status_code == 200:
            resultado_json = response.json()
            return resultado_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"❌ Error de Servidor Google: Code {response.status_code}"
    except Exception as e:
        return f"❌ Fallo crítico de comunicación Gemini: {str(e)}"

def enviar_mensaje_telegram(token, chat_id, texto):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ Error al enviar a Telegram: {e}")

def iniciar_bot_telegram():
    # Recuperación limpia y segura desde variables de entorno de Linux
    token = os.getenv("M82_TELEGRAM_TOKEN", "").strip()
    chat_id = os.getenv("M82_TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id:
        print("❌ ERROR: Faltan configurar variables de Telegram en tu Termux.")
        print("👉 Debes ejecutar los comandos 'export M82_TELEGRAM_TOKEN=...' y 'export M82_TELEGRAM_CHAT_ID=...'")
        return

    print("🛰️ [M82 Bot] Servidor de Telegram en línea y escuchando comandos...")
    enviar_mensaje_telegram(token, chat_id, "🚀 **Monolito M82 Soberano en línea.** Envía el comando `/reporte` en tu Telegram para actualización instantánea.")
    
    last_update_id = 0
    url_updates = f"https://api.telegram.org/bot{token}/getUpdates"
    
    while True:
        try:
            response = requests.get(url_updates, params={"offset": last_update_id + 1, "timeout": 20}, timeout=25)
            if response.status_code == 200:
                data = response.json()
                for update in data.get("result", []):
                    last_update_id = update["update_id"]
                    message = update.get("message", {})
                    texto_recibido = message.get("text", "").strip()
                    
                    if texto_recibido == "/reporte":
                        print("📥 Comando /reporte solicitado mediante Telegram. Procesando...")
                        enviar_mensaje_telegram(token, chat_id, "⏳ *Conectando al núcleo C++ y barriendo mercados con Gemini en tiempo real...*")
                        
                        # Ejecutar motor híbrido
                        reporte = ejecutar_monolito_hibrido()
                        
                        # Enviar respuesta directo al bot
                        enviar_mensaje_telegram(token, chat_id, reporte)
                        print("📤 Reporte de alta velocidad transmitido a Telegram con éxito.")
                        
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nApagando M82 Core de forma segura.")
            break
        except Exception as e:
            print(f"⚠️ Alerta en bucle de escucha: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_bot_telegram()
