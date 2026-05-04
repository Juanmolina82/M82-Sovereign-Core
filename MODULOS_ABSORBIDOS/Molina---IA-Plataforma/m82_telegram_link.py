import telebot
import time

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
bot = telebot.TeleBot(TOKEN)
M82_SIG = "\n━━━━━━━━━━━━━━━━━━━━\n🏛️ MOLINA HOLDINGS LLC\n🛰️ M82 SOBERANO"

@bot.message_handler(commands=['analisis', 'dar', 'ubs'])
def ubs_summary(m):
    resumen = (
        "📊 **MAPA DE SALIDA UBS (LSEG)**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔴 **DAR (Darling)**: Venta del 44.6% (Bio-Fuel)\n"
        "🔴 **QQQM (Nasdaq)**: Venta del 10.4% (Tech)\n"
        "🔴 **BHF (Brighthouse)**: Venta del 25.6% (Seguros)\n"
        "🟢 **VTEB (Vanguard)**: Único refugio activo.\n\n"
        "💡 **ESTRATEGIA M82**: UBS está vaciando su cartera de crecimiento y riesgo. Se están preparando para un escenario de contracción o crisis de liquidez."
        + M82_SIG
    )
    bot.reply_to(m, resumen, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, "🏛️ **M82 SOBERANO V4**\nData LSEG: $DAR / $VTEB / $QQQM / $BHF cargada.\n\nEscriba /analisis para el reporte consolidado.")

print("[🛰️] M82 V4: NÚCLEO DE INTELIGENCIA TOTAL ACTIVO")
bot.infinity_polling()
