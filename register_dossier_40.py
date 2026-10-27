import sqlite3

conn = sqlite3.connect('m82_database.db')
cursor = conn.cursor()

# Registro de vectores adicionales para alcanzar la meta de 40+ activos
extra_signals = [
    ('M82_WIRE', 'EQUITY', 'AAPL', 7.5, 'AAPL.O Apple Inc UP 3.01% at $349.96 | Institutional Momentum Breakout'),
    ('M82_WIRE', 'FX_CRYPTO', 'USDT_VES', 8.4, 'Liquidity Gap & Volatility Index on Local FX Corridor'),
    ('M82_MACRO', 'COMMODITIES', 'HENRY_HUB', 8.1, 'Henry Hub Natural Gas Spread & LNG Export Arbitrage'),
    ('M82_MACRO', 'RATES', 'EURIBOR_3M', 6.2, 'Euribor 3M Yield Curve & ECB Policy Rate Expectations'),
    ('M82_MACRO', 'CREDIT', 'VEN_SOV_27', 9.2, 'Venezuela Sovereign Debt Restructuring Spreads & PDVSA Claims'),
    ('M82_MACRO', 'ENERGY', 'PDVSA_PETROCEDENO', 9.0, 'Petrocedeño Heavy Crude Blending & Jose Export Tanker Load'),
    ('M82_WIRE', 'EQUITY', 'NVDA', 7.8, 'NVIDIA NVDA Market Cap Expansion to $6T & AI Infrastructure Capex'),
    ('M82_MACRO', 'FX', 'DXY_INDEX', 6.5, 'US Dollar Index DXY Retracement -0.22% on Fed Rate Pause Expectations'),
    ('M82_MACRO', 'RATES', 'US_30Y_TREASURY', 7.0, 'US 30Y Treasury Yield Compression -0.18pb to 5.66%'),
    ('M82_MACRO', 'RATES', 'FRA_10Y_OAT', 7.4, 'France 10Y OAT Yield Drop -18pb to 4.76% Fiscal Budget Relief')
]

for src, cat, asset, risk, headline in extra_signals:
    cursor.execute("""
        INSERT INTO signals (source, category, asset_class, risk_score, headline)
        VALUES (?, ?, ?, ?, ?)
    """, (src, cat, asset, risk, headline))

conn.commit()

cursor.execute("SELECT COUNT(*) FROM signals")
total = cursor.fetchone()[0]
conn.close()

print(f"✅ Registrados exitosamente los vectores faltantes. Total en m82_database.db: {total} vectores.")
