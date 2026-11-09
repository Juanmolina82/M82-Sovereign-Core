import json
from datetime import datetime

payload = {
  "event_code": "M82_L3_GEOMACRO_FUSION_2026_09_M82_MACRO",
  "timestamp": "2026-09-22 07:09:53",
  "market_snapshot": {
    "brent_ice_settle": 104.63,
    "wti_nymex": 102.00,
    "dubai_physical_premium": 14.65,
    "oman_swap_premium": 28.47,
    "vlcc_meg_china_tce_usd": 1250000,
    "fujairah_anchorage_congestion": 120,
    "structure": "EXTREME_PHYSICAL_SOUR_SHORTAGE"
  },
  "vectors": {
    "ormuz_strait": {"transits_per_day": 6, "deficit_pct": -70.0, "effective_flow_mbpd": 4.20},
    "petroline_saudi": {"status": "OFFLINE_YANBU_SUSPENDED", "capacity_lost_mbpd": 4.50},
    "western_hemisphere": {
      "thesis": "John Kemp / M82 Wire",
      "atlantic_heavy_crude_monopoly": "VENEZUELA",
      "pacto_discount_usd": -40.00,
      "net_realized_price_usd": 64.63,
      "captured_value_loss_usd": 54.65
    }
  }
}

def calc_arbitrage(payload, export_bpd=400000):
    brent = payload["market_snapshot"]["brent_ice_settle"]
    dubai_prem = payload["market_snapshot"]["dubai_physical_premium"]
    oman_prem = payload["market_snapshot"]["oman_swap_premium"]
    discount = payload["vectors"]["western_hemisphere"]["pacto_discount_usd"]
    
    dubai_physical = brent + dubai_prem
    oman_physical = brent + oman_prem
    net_realized = brent + discount
    loss_vs_dubai = dubai_physical - net_realized
    loss_vs_oman = oman_physical - net_realized
    
    annual_loss_dubai = loss_vs_dubai * export_bpd * 365 / 1e9
    annual_loss_oman = loss_vs_oman * export_bpd * 365 / 1e9
    
    return {
        "dubai_physical": round(dubai_physical,2),
        "oman_physical": round(oman_physical,2),
        "net_realized": round(net_realized,2),
        "loss_vs_dubai_bbl": round(loss_vs_dubai,2),
        "loss_vs_oman_bbl": round(loss_vs_oman,2),
        "annual_loss_dubai_B": round(annual_loss_dubai,2),
        "annual_loss_oman_B": round(annual_loss_oman,2),
        "vlcc_signal": "EXTREME" if payload["market_snapshot"]["vlcc_meg_china_tce_usd"] > 1000000 else "NORMAL"
    }

if __name__ == "__main__":
    result = calc_arbitrage(payload)
    print(json.dumps(result, indent=2))
