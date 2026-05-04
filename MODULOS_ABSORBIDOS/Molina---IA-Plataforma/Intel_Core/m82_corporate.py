import requests
import time

TOKEN = '8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4'

def m82_polymath_engine(text):
    msg = text.lower()
    
    # VECTOR 1: GEOPOLÍTICA E INFRAESTRUCTURA (CUBA / CARIBE)
    if any(w in msg for w in ['cuba', 'havana', 'caribbean', 'maritime']):
        topic = "Sovereign Risk & Caribbean Maritime Logistics"
        analysis = (
            "The geopolitical recalibration of the Caribbean basin is creating a vacuum in infrastructure leadership. "
            "Monitoring Cuba's strategic deep-water capabilities and sovereign debt shifts is mandatory for regional asset protection."
        )
        sentiment = "High Vigilance / Risk Mitigation"
        tags = "#Geopolitics #SovereignRisk #CaribbeanLogistics #Infrastructure #MolinaHoldings"

    # VECTOR 2: ENERGÍA FÍSICA Y ESCASEZ (WOODSIDE / OIL / LNG)
    elif any(w in msg for w in ['woodside', 'oil', 'brent', 'lng', 'crude', 'opec', 'inventory']):
        topic = "Physical Scarcity & Upstream Capex Fragility"
        analysis = (
            "Operational disruptions in majors like Woodside are symptoms of a thinning global safety buffer. "
            "We reiterate our $125.5 terminal price thesis, driven by the decoupling of paper markets from physical delivery realities."
        )
        sentiment = "High Conviction / Bullish"
        tags = "#EnergyMarkets #OilAndGas #LNG #Commodities #OPEC #MolinaHoldings"

    # VECTOR 3: MACRO-POLÍTICA Y FLUJOS DE CAPITAL (TRUMP / FED / SENATE)
    elif any(w in msg for w in ['trump', 'senate', 'policy', 'trade', 'federal']):
        topic = "Macro-Policy Volatility & Institutional Hedging"
        analysis = (
            "Fiscal policy shifts in the U.S. are redefining the cost of capital globally. "
            "The transition towards protectionist trade frameworks necessitates a pivot to sovereign-backed hard assets."
        )
        sentiment = "Tactical Realignment"
        tags = "#MacroEconomics #CapitalMarkets #PrivateEquity #FiscalPolicy #MolinaHoldings"

    else:
        topic = "Multi-Asset Strategy & Sovereign Intelligence"
        analysis = "Translating global volatility into institutional alpha through rigorous quantitative vetting and geopolitical foresight."
        sentiment = "Analytical / Neutral"
        tags = "#HedgeFund #InvestmentStrategy #AlphaGeneration #MolinaHoldings"

    return (
        f"🏛️ **MOLINA HOLDINGS | STRATEGIC INTELLIGENCE**\n\n"
        f"**Sector Focus:** {topic}\n"
        f"**Technical Analysis:** {analysis}\n"
        f"**Strategic Sentiment:** {sentiment}\n\n"
        f"---\n"
        f"{tags}"
    )

def start_bunker():
    last_id, s = 0, requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0'})
    print("🚀 M82 POLYMATH: ONLINE")
    while True:
        try:
            r = s.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id+1}&timeout=5', timeout=10).json()
            for u in r.get('result', []):
                last_id = u['update_id']
                if 'message' in u and 'text' in u['message']:
                    res = m82_polymath_engine(u['message']['text'])
                    s.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', json={'chat_id': u['message']['chat']['id'], 'text': res})
        except: time.sleep(0.1)

if __name__ == "__main__":
    start_bunker()
