import sqlite3, os, time, random

DB_PATH = os.path.expanduser('~/M82/m82_database.db')

DAEMONS = [
    'REFINITIV_ENERGY_DESK', 'GLOBAL_MACRO_FED', 'CITGO_VALUATION_DESK',
    'PERIMETER_MONITOR', 'QUANTUM_ALPHA_ENGINE', 'WARSH_SPREAD_WATCH'
]

HEADLINES = [
    "Merey 16 Spot Premium holds +$2.40/bbl — Quad-SPV Settlement Executed",
    "Warsh Spread variance stable at +102bps — Exposure Lock 0.30x verified",
    "Citgo Restructuring Mandate: $2.1B Bond Recovery Tranche Approved",
    "Goldman Marquee Signal: BUY MEREY16 Anchor — Volatility Index 1.68%",
    "Quantum Scoring: Alpha score 0.9400 entangled with sentiment matrix"
]

IMPACTS = ['MEREY16_BUY', 'MACRO_STABLE', 'CITGO_BOND_RECOVERY', 'BUNKER_LOCK']

def pump_light():
    print("⚡ [M82 LIGHTWEIGHT PUMP] Bombeo de estabilidad optimizado (12s)...")
    while True:
        try:
            conn = sqlite3.connect(DB_PATH, timeout=15)
            conn.execute('PRAGMA journal_mode=WAL;')
            conn.execute('PRAGMA synchronous=NORMAL;')
            
            daemon = random.choice(DAEMONS)
            headline = random.choice(HEADLINES)
            impact = random.choice(IMPACTS)
            alpha = round(random.uniform(0.85, 0.98), 2)
            sentiment = round(random.uniform(0.75, 0.92), 2)
            
            conn.execute('''
                INSERT INTO m82_multi_stream (daemon_source, headline, status, alpha_score, sentiment, asset_impact, event_trigger)
                VALUES (?, ?, 'PENDING', ?, ?, ?, 'AGI_QUANTUM_SIGNAL')
            ''', (daemon, headline, alpha, sentiment, impact))
            
            conn.commit()
            conn.close()
        except Exception as e:
            pass
            
        time.sleep(12)  # Frecuencia moderada para evitar cierres de Android

if __name__ == '__main__':
    pump_light()
