import requests
import os

TOKEN = "7876800049:AAGD2U86Zid9E96z8vYl8yHicB_O_37996c"
CHAT_ID = "7410312683"

def main():
    message = "🏛️ **MOLINA GLOBAL - ESTATUS DE MONITOREO**\n"
    message += "✅ El sistema ha sido re-sincronizado post-purga.\n"
    message += "🛡️ **Contexto Axios:** Vigilancia de activos navales activa.\n"
    message += "📊 **Jurisdicción:** Master Architecture V3.2."
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    main()
