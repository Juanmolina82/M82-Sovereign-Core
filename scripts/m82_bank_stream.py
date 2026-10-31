import os, json, pandas as pd

def generate_m82_breaking_streams():
    data_dir = os.path.expanduser("~/M82/data")
    os.makedirs(data_dir, exist_ok=True)

    banks_data = [
        {
            "ticker": "WFC", "name": "WELLS FARGO", "revenue": "$21.87B", "revenue_yoy": "-2.02%", "rev_status": "MISS",
            "net_income": "$5.90B", "net_income_yoy": "+6.40%", "net_status": "BEAT", "eps": "$1.87", "eps_yoy": "+12.00%",
            "eps_prev": "$1.66", "roe": "13.8%", "roe_prev": "12.8%", "premarket": "$82.60", "premarket_change": "+1.04%",
            "ceo_quote": "Consumidor y clientes comerciales saludables. Morosidad baja y expansión en depósitos e inversión."
        },
        {
            "ticker": "JPM", "name": "JPMORGAN CHASE", "revenue": "$43.32B", "revenue_yoy": "+6.50%", "rev_status": "BEAT",
            "net_income": "$12.90B", "net_income_yoy": "+1.80%", "net_status": "BEAT", "eps": "$4.37", "eps_yoy": "+12.30%",
            "eps_prev": "$3.89", "roe": "17.0%", "roe_prev": "16.2%", "premarket": "$224.50", "premarket_change": "+1.85%",
            "ceo_quote": "La economía de EE.UU. se mantiene firme, aunque persisten riesgos geopolíticos y presiones inflacionarias."
        },
        {
            "ticker": "BAC", "name": "BANK OF AMERICA", "revenue": "$25.49B", "revenue_yoy": "+0.70%", "rev_status": "BEAT",
            "net_income": "$6.90B", "net_income_yoy": "-12.00%", "net_status": "MISS", "eps": "$0.81", "eps_yoy": "-9.00%",
            "eps_prev": "$0.89", "roe": "10.8%", "roe_prev": "11.2%", "premarket": "$42.10", "premarket_change": "-0.75%",
            "ceo_quote": "Crecimiento constante de clientes y calidad crediticia sólida en toda la franquicia comercial."
        },
        {
            "ticker": "C", "name": "CITIGROUP", "revenue": "$20.32B", "revenue_yoy": "+1.10%", "rev_status": "BEAT",
            "net_income": "$3.20B", "net_income_yoy": "-8.50%", "net_status": "BEAT", "eps": "$1.51", "eps_yoy": "-7.30%",
            "eps_prev": "$1.63", "roe": "7.0%", "roe_prev": "7.7%", "premarket": "$66.80", "premarket_change": "+1.20%",
            "ceo_quote": "Nuestra transformación avanza según lo planificado, impulsando la eficiencia operativa y retornos clave."
        },
        {
            "ticker": "GS", "name": "GOLDMAN SACHS", "revenue": "$12.70B", "revenue_yoy": "+7.50%", "rev_status": "BEAT",
            "net_income": "$2.99B", "net_income_yoy": "+45.00%", "net_status": "BEAT", "eps": "$8.40", "eps_yoy": "+53.50%",
            "eps_prev": "$5.47", "roe": "10.4%", "roe_prev": "7.1%", "premarket": "$525.00", "premarket_change": "+2.40%",
            "ceo_quote": "Fuerte reactivación en banca de inversión y operaciones de capitales impulsa el desempeño trimestral."
        },
        {
            "ticker": "MS", "name": "MORGAN STANLEY", "revenue": "$15.38B", "revenue_yoy": "+15.30%", "rev_status": "BEAT",
            "net_income": "$3.19B", "net_income_yoy": "+32.00%", "net_status": "BEAT", "eps": "$1.88", "eps_yoy": "+36.20%",
            "eps_prev": "$1.38", "roe": "13.1%", "roe_prev": "10.6%", "premarket": "$112.30", "premarket_change": "+3.10%",
            "ceo_quote": "Sólido crecimiento de activos bajo gestión en Wealth Management y fuerte actividad en trading."
        }
    ]

    print("\n" + "="*60)
    print("      M82 BREAKING STREAM :: BANKING DESK (Q3 2026)")
    print("="*60 + "\n")

    for b in banks_data:
        stream_msg = (
            f"🚨 #M82 BREAKING STREAM {b['ticker']}_EARNINGS_DESK\n\n"
            f"🏦 {b['name']} Q3 2026 EARNINGS\n"
            f"• Revenue: {b['revenue']} ({b['revenue_yoy']} YoY) {b['rev_status']}\n"
            f"• Net Income: {b['net_income']} ({b['net_income_yoy']} YoY) {b['net_status']}\n"
            f"• EPS: {b['eps']} ({b['eps_yoy']} YoY vs {b['eps_prev']} 2025)\n"
            f"• ROE: {b['roe']} (vs {b['roe_prev']} 2025)\n"
            f"• Pre-Market: {b['premarket']} ({b['premarket_change']})\n\n"
            f"📌 CEO: '{b['ceo_quote']}'\n\n"
            f"🏛 @MolinaHoldings | AGI Quantum Node\n"
            f"🔒 BUNKER MODE 0.30x LOCK\n"
            f"{'-'*60}"
        )
        print(stream_msg)

    bot_file = os.path.join(data_dir, "m82_bank_bot_stream.json")
    with open(bot_file, "w") as f:
        json.dump({"desk": "M82_BANKING_DESK", "count": len(banks_data), "streams": banks_data}, f, indent=4)

    df = pd.DataFrame(banks_data)
    nyft_file = os.path.join(data_dir, "m82_bank_nyft_stream.csv")
    df.to_csv(nyft_file, index=False)
    print(f"[✓] Feeds exportados correctamente en: {data_dir}\n")

if __name__ == "__main__":
    generate_m82_breaking_streams()
