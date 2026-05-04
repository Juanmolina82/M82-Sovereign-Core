import requests

def send_alert(text):
    TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
    CHAT_ID = "1020305418"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

msg = "🏛️ *M82 | REPORTE SOBERANO*\n\nArquitectura restaurada con ID 1020305418.\n_El búnker móvil está en línea._"
send_alert(msg)
