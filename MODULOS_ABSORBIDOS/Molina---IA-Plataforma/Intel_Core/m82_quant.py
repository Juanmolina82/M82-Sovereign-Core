import requests
import time
from datetime import datetime

TOKEN = '8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4'

def get_market_context(text):
    msg = text.lower()
    
    # 🇻🇪 VECTOR VENEZUELA: ARBITRAJE SOBERANO Y ENERGÍA
    if any(w in msg for w in ['venezuela', 'pdvsa', 'caracas', 'bcv']):
        return {
            "sector": "Sovereign Arbitrage & Energy Dominance",
            "analysis": "Venezuela is the global lynchpin for non-OPEC+ supply stability. Beyond the political noise, the underlying asset value and infrastructure potential represent the highest asymmetric reward in the hemisphere. We are looking at a 'Sovereign Pivot' where energy reliability overrides outdated sanction frameworks.",
            "thesis": "Aggressive Long: Infrastructure integration + debt restructuring. The $125.5 floor is reinforced by Venezuelan supply-side logistics.",
            "tags": "#VenezuelaSovereign #EnergyArbitrage #PDVSA #EmergingMarkets #MolinaHoldings"
        }
    
    # 🇮🇷 VECTOR GEOPOLÍTICA (IRÁN / MEDIO ORIENTE)
    elif any(w in msg for w in ['iran', 'hormuz', 'israel', 'tehran']):
        return {
            "sector": "Geopolitical Strategic Hedging",
            "analysis": "Structural instability in the Strait of Hormuz is not a risk; it is a permanent variable. Every barrel from the Middle East now carries a 'War Premium' that institutional capital must hedge through Western-aligned hard assets.",
            "thesis": "High Conviction: Pivot to secure Atlantic-basin production nodes.",
            "tags": "#MacroRisk #Hormuz #SovereignRisk #HedgeFund"
        }

    # 🛢️ VECTOR ENERGÍA FÍSICA (OIL / WOODSIDE)
    elif any(w in msg for w in ['oil', 'brent', 'wti', 'woodside', 'lng']):
        return {
            "sector": "Physical Commodity Arbitrage",
            "analysis": "The decoupling of physical delivery from paper markets is reaching a critical inflection point. Supply-side constraints in majors (e.g. Woodside) prove that scarcity is the new macro driver.",
            "thesis": "Bullish: Structural floor at $125.5/bbl due to chronic underinvestment.",
            "tags": "#OilAndGas #PhysicalMarkets #LNG #OPEC"
        }

    return {
        "sector": "Institutional Multi-Asset Intelligence",
        "analysis": "Monitoring volatility spikes. Our focus remains on high-conviction signals within sovereign-backed energy sectors.",
        "thesis": "Neutralizing noise through quantitative alpha.",
        "tags": "#HedgeFund #PortfolioStrategy #MolinaHoldings"
    }

def start_bunker():
    last_id, s = 0, requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0'})
    print(f"🚀 M82 VENEZUELA-ALPHA ACTIVE | {datetime.now()}")
    
    while True:
        try:
            r = s.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id+1}&timeout=0', timeout=2).json()
            if r.get('result'):
                for u in r['result']:
                    last_id = u['update_id']
                    if 'message' in u and 'text' in u['message']:
                        ctx = get_market_context(u['message']['text'])
                        
                        response = (
                            f"🏛️ **MOLINA HOLDINGS | QUANT INTEL**\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"📂 **Sector:** {ctx['sector']}\n\n"
                            f"🧠 **Technical Analysis:**\n{ctx['analysis']}\n\n"
                            f"⚖️ **Fund Thesis:**\n{ctx['thesis']}\n\n"
                            f"🛡️ **Strategic Tags:**\n{ctx['tags']}\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━"
                        )
                        s.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', 
                               json={'chat_id': u['message']['chat']['id'], 'text': response, 'parse_mode': 'Markdown'})
        except Exception:
            time.sleep(0.1)

if __name__ == "__main__":
    start_bunker()
