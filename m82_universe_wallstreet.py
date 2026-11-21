# M82 UNIVERSE - Wall Street Completo - Refinitiv RICs
UNIVERSE = {
    "indices": [".SPX", ".DJI", ".IXIC", ".RUT", ".VIX", ".SOX"],
    "mega_cap": ["AAPL.O", "MSFT.O", "NVDA.O", "AMZN.O", "GOOGL.O", "META.O", "TSLA.O", "AVGO.O", "LLY.N"],
    "ai_semis": ["NVDA.O", "AMD.O", "TSM.N", "AVGO.O", "MRVL.O", "MU.O", "KLAC.O", "LRCX.O", "ASML.O", "ARM.O"],
    "ai_infra": ["MSFT.O", "ORCL.N", "CRWV.O", "NBIS.O", "PLTR.N", "ANET.N", "DELL.N", "SMCI.O"],
    "banks": ["JPM.N", "BAC.N", "GS.N", "MS.N", "WFC.N", "C.N", "UCG.MI"],
    "energy": ["XOM.N", "CVX.N", "SHEL.N", "CLc1", "LCOc1", "NGc1", "XAU=", "XAG="],
    "crypto_proxy": ["COIN.O", "MSTR.O", "BTC=", "ETH="],
    "rates_fx": ["US10YT=RR", "US2YT=RR", "EUR=", "JPY=", "DXY"],
    "etfs_core": ["SPY.N", "QQQ.O", "DIA.N", "IWM.N", "XLK.N", "XLF.N", "XLE.N"],
    "private_ai": ["ANT.O", "OPENAI.PVT", "ANTHROPIC.PVT"],
    "m82_watch": ["9984.T", "0700.HK", "005930.KS", "INTC.O", "TMO.N"],
}
# Total: ~60 RICs - Cobertura completa Wall Street + Asia + Commodities
print(f"[UNIVERSE OK] {sum(len(v) for v in UNIVERSE.values())} RICs cargados")
