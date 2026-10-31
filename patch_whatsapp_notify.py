import os

orchestrator_path = os.path.expanduser("~/M82/m82_core_orchestrator.py")

notify_function = """
import requests

def notify_whatsapp(text_body):
    try:
        url = "http://127.0.0.1:8085/send-alert"
        payload = {"message": text_body}
        requests.post(url, json=payload, timeout=3)
    except Exception as e:
        pass
"""

with open(orchestrator_path, "a") as f:
    f.write("\n" + notify_function + "\n")

print("✅ Notificador de WhatsApp vinculado al Orquestador M82.")
