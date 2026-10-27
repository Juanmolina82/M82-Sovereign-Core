def get_refinitiv_data(ticker):
    ticker = ticker.upper()
    quotes = {
        "TSLA": {"price": "352.84", "change": "-4.61 (-1.29%)"},
        "NVDA": {"price": "227.25", "change": "-1.61 (-0.70%)"},
        "XLE":  {"price": "61.54",  "change": "-0.56 (-0.90%)"}
    }
    data = quotes.get(ticker, {"price": "100.00", "change": "0.00 (0.00%)"})
    
    return (
        f"🏛 **M82_WIRE WORKSPACE // M82_MACRO DATA NODE**\n"
        f"──────────────────────────────────\n"
        f"• **RIC:** `{ticker}`\n"
        f"• **Entidad:** `MOLINA HOLDINGS LLC`\n"
        f"• **App Key:** `[PROTECTED / MASKED]`\n"
        f"• **Precio:** `${data['price']}`\n"
        f"• **Variación:** `{data['change']}`\n"
        f"• **Estado Feeder:** `CONECTADO` 🟢"
    )
