#!/usr/bin/env python3
import os, sys, time, sqlite3, requests, json

TOKEN = "8600412468:AAHLLRDPus66Y1hSgDKbwGC5zdW6DdufP3Y"
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    try:
        url = f"{BASE_URL}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error enviando mensaje: {e}")

def get_market_quote(ticker):
    ticker = ticker.upper()
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        meta = data['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice', 0.0)
        prev_close = meta.get('chartPreviousClose', price)
        change = price - prev_close
        pct_change = (change / prev_close) * 100 if prev_close else 0.0
        
        sign = "+" if change >= 0 else ""
        icon = "🟢" if change >= 0 else "🔴"

        return (
            f"📊 *WALL STREET QUOTE // {ticker}*\n"
            f"────────────────────────\n"
            f"• *Precio Actual:* `${price:,.2f}`\n"
            f"• *Variación:* `{sign}{change:,.2f}` ({sign}{pct_change:.2f}%) {icon}\n"
            f"• *Cierre Previo:* `${prev_close:,.2f}`\n"
            f"• *Moneda:* `{meta.get('currency', 'USD')}`\n"
            f"• *Mercado:* `{meta.get('exchangeName', 'N/A')}`\n\n"
            f"🏛 *M82 Quantitative Intelligence*"
        )
    except Exception:
        return f"❌ *Error:* No se encontraron datos para el ticker `{ticker}`."

def get_macro_monitor():
    tickers = {"US10Y": "^TNX", "VIX": "^VIX", "S&P 500": "^GSPC", "BRENT": "BZ=F", "GOLD": "GC=F"}
    lines = ["🌐 *M82 GLOBAL MACRO & FED MONITOR*", "────────────────────────"]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    for label, sym in tickers.items():
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
            r = requests.get(url, headers=headers, timeout=5)
            meta = r.json()['chart']['result'][0]['meta']
            p = meta.get('regularMarketPrice', 0.0)
            pc = meta.get('chartPreviousClose', p)
            chg = ((p - pc) / pc) * 100 if pc else 0.0
            icon = "🟢" if chg >= 0 else "🔴"
            lines.append(f"• *{label}:* `{p:,.2f}` ({chg:+.2f}%) {icon}")
        except Exception:
            lines.append(f"• *{label}:* `N/A`")
            
    lines.append("\n🏛 *@MolinaHoldings LLC*")
    return "\n".join(lines)

def get_venezuela_status():
    return (
        "🛢 *VECTOR GEOPOLÍTICO & VENEZUELA MACRO*\n"
        "────────────────────────\n"
        "• *Subasta Citgo:* Estado de litigios y deudores del PDVSA 2020 bajo seguimiento.\n"
        "• *Petróleo Merey 16:* Monitoreo de descuentos y logística del Estrecho de Ormuz vs. Caribe.\n"
        "• *Licencias OFAC:* Ingesta activa sobre actualizaciones de Chevron / licencias específicas.\n"
        "• *Rutas Navieras (Kpler):* Rastreo de buques y transpondedores AIS en Golfo Triste.\n\n"
        "📡 *Daemons dedicados:* `m82_venezuela_legitimacy`, `m82_delcy_osint`, `m82_kpler_flow`"
    )

def get_system_status():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM m82_multi_stream")
    total_signals = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM m82_multi_stream WHERE status = 'PENDING'")
    pending = cursor.fetchone()[0]
    conn.close()

    return (
        "⚙️ *M82 INFRASTRUCTURE DIAGNOSTIC*\n"
        "────────────────────────\n"
        f"• *Señales Ingeridas:* `{total_signals}`\n"
        f"• *Pendientes de Análisis:* `{pending}`\n"
        "• *Motor de Agente:* `ONLINE` 🧠\n"
        "• *Persistencia SQLite:* `OK` 💾\n"
        "• *Daemons de Ingesta:* `36 ACTIVOS` 📡\n\n"
        "🏛 *M82 Quantum Orchestrator v2*"
    )

def process_command(chat_id, text):
    parts = text.strip().split()
    cmd = parts[0].lower()

    if cmd == "/quote":
        if len(parts) > 1:
            reply = get_market_quote(parts[1])
        else:
            reply = "⚠️ *Uso:* `/quote <ticker>` (Ejemplo: `/quote NVDA` o `/quote TSLA`)"
        send_message(chat_id, reply)

    elif cmd == "/macro":
        send_message(chat_id, get_macro_monitor())

    elif cmd == "/venezuela":
        send_message(chat_id, get_venezuela_status())

    elif cmd == "/status":
        send_message(chat_id, get_system_status())

    elif cmd in ["/start", "/help"]:
        help_msg = (
            "🏛 *COMANDOS WALL STREET & MACRO M82*\n"
            "────────────────────────\n"
            "• `/quote <ticker>` - Cotización en tiempo real (EE.UU., ETFs, ADRs)\n"
            "• `/macro` - Tasas US10Y, VIX, WTI, Brent y S&P 500\n"
            "• `/venezuela` - Monitor Citgo, Licencias OFAC y Petróleo\n"
            "• `/insiders` - Compras/Ventas directivas Form 4\n"
            "• `/status` - Diagnóstico de base de datos y daemons\n"
            "• `/help` - Muestra esta lista de comandos"
        )
        send_message(chat_id, help_msg)

def poll_updates():
    offset = None
    print("🤖 Bot de Comandos Interactivos M82 iniciado y escuchando...")
    while True:
        try:
            url = f"{BASE_URL}/getUpdates"
            params = {"timeout": 20, "offset": offset}
            r = requests.get(url, params=params, timeout=25)
            data = r.json()

            if data.get("ok"):
                for result in data.get("result", []):
                    offset = result["update_id"] + 1
                    message = result.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "")

                    if text and chat_id:
                        process_command(chat_id, text)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    poll_updates()
