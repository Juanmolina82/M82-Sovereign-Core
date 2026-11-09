import requests, sqlite3, os
from datetime import datetime
from gtts import gTTS

# Configurar o leer de entorno
BOT_TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
CHAT_ID = "-1004335849125"
DB = os.path.expanduser("~/M82/m82_database.db")

def send_voice_summary():

    # Throttle: Enviar voz solo si hay PENDING en los últimos 6 minutos
    conn = sqlite3.connect(DB)
    recent_pending = conn.execute("""
        SELECT COUNT(*) FROM m82_multi_stream 
        WHERE status='PENDING' AND created_at > datetime('now', '-6 minutes')
    """).fetchone()[0]
    conn.close()

    if recent_pending == 0:
        print('⏳ [THROTTLE VOICE] Sin eventos PENDING nuevos en los últimos 6 min. Omitiendo audio.')
        return

    if BOT_TOKEN == "TU_TOKEN_AQUI" or CHAT_ID == "TU_CHAT_ID":
        print("⚠️ Configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID para enviar audio.")
        return

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    pending = c.execute("""
        SELECT asset_impact, final_score 
        FROM m82_multi_stream 
        WHERE status='PENDING' AND date(created_at)=date('now') 
        ORDER BY final_score DESC LIMIT 5
    """).fetchall()

    skipped = c.execute("""
        SELECT COUNT(*) 
        FROM m82_multi_stream 
        WHERE status='SKIPPED_LOW_EV' AND date(created_at)=date('now')
    """).fetchone()[0]

    conn.close()

    if not pending:
        texto = f"Mesa M82 Molina Holdings. Resumen actual. Sin señales de alto EV. {skipped} oportunidades descartadas por filtro de riesgo. Drenaje de liquidez en menos 176 billones. Manteniendo posicionamiento defensivo."
    else:
        lista = ", ".join([f"{t[0]} con score {t[1]}" for t in pending])
        texto = f"Informe ejecutivo DANEKA M82. {len(pending)} señales activas. {lista}. {skipped} filtradas por bajo EV. Factor de tamaño al 50 por ciento por drenaje de liquidez."

    print(f"🎙️ [SÍNTESIS DE VOZ]: {texto}")

    # Generar MP3
    audio_path = "/data/data/com.termux/files/home/M82/m82_summary.mp3"
    tts = gTTS(texto, lang='es', slow=False)
    tts.save(audio_path)

    # Enviar Voice Note a Telegram
    try:
        with open(audio_path, "rb") as audio:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVoice"
            res = requests.post(
                url, 
                data={"chat_id": CHAT_ID, "caption": "🏛️ DANEKA M82 / @MolinaHoldings LLC — Audio Executive Update"}, 
                files={"voice": audio},
                timeout=10
            )
            if res.status_code == 200:
                print("✅ [TELEGRAM VOICE] Audio enviado con éxito.")
            else:
                print(f"❌ Error Telegram: {res.text}")
    except Exception as e:
        print(f"❌ Excepción al enviar audio: {e}")

if __name__ == "__main__":
    send_voice_summary()
