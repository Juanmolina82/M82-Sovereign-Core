#!/usr/bin/env bash
set -e

echo "=================================================="
echo "⚙️ INSTALANDO ARQUITECTURA DE DAEMONS M82 (WAL MODE)"
echo "=================================================="

BASE_DIR="$HOME/M82"
DAEMONS_DIR="$BASE_DIR/daemons"
mkdir -p "$DAEMONS_DIR"

# ----------------------------------------------------
# 1. DAEMON: M82_WIRE WORLD & TECH NEWS
# ----------------------------------------------------
cat << 'PYEOF' > "$DAEMONS_DIR/daemon_refinitiv_world.py"
#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

feeds = [
    {"source": "M82_WIRE_AI", "headline": "Anthropic IPO prospectus shows sweeping AI vision, surging costs"},
    {"source": "M82_WIRE_MARKETS", "headline": "Nvidia sets biggest-ever buyback plan as AI chip competition weighs on stock"},
    {"source": "M82_WIRE_GEO", "headline": "US, Iran separately talk with mediators in latest bid to end war"},
    {"source": "M82_WIRE_TRADE", "headline": "China, US pledge tariff cuts on $60 billion of goods including agriculture, toys"},
    {"source": "M82_WIRE_TECH", "headline": "SpaceX Starship makes orbital debut deploying Starlinks before early landing"},
    {"source": "M82_WIRE_AI_SAFETY", "headline": "OpenAI Scraps Release of New AI Model Over Safety Concerns"},
    {"source": "M82_WIRE_DEFENSE", "headline": "Raytheon Gets $20.7 Billion Contract to Accelerate AMRAAM Missile Production"}
]

def run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    count = 0
    for item in feeds:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (item["source"], item["headline"], now))
        if c.rowcount > 0: count += 1
        
    conn.commit()
    conn.close()
    print(f"🤖 [DAEMON WORLD]: Inyectadas {count} nuevas señales.")

if __name__ == "__main__":
    run()
PYEOF

# ----------------------------------------------------
# 2. DAEMON: VENEZUELA POLITICS & DESK
# ----------------------------------------------------
cat << 'PYEOF' > "$DAEMONS_DIR/daemon_ve_politics.py"
#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

feeds = [
    {"source": "VE_DESK_EXILE", "headline": "VENEZUELA: Jefa de comunicaciones de Maria Corina Machado regresa tras 1.5 años de exilio"},
    {"source": "VE_DESK_MOBILIZE", "headline": "VENEZUELA MOBILIZATION: Supporters of Maria Corina Machado mobilize demanding safe return and elections"},
    {"source": "VE_DESK_DIPLOMACY", "headline": "VENEZUELA GEOPOLITICS: International pressure grows for transparent electoral roadmap in Venezuela"}
]

def run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    count = 0
    for item in feeds:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (item["source"], item["headline"], now))
        if c.rowcount > 0: count += 1
        
    conn.commit()
    conn.close()
    print(f"🇻🇪 [DAEMON VENEZUELA]: Inyectadas {count} nuevas señales.")

if __name__ == "__main__":
    run()
PYEOF

# ----------------------------------------------------
# 3. DAEMON: MACRO, YIELDS & ENERGY
# ----------------------------------------------------
cat << 'PYEOF' > "$DAEMONS_DIR/daemon_macro_yields.py"
#!/usr/bin/env python3
import sqlite3, os, datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")

def run():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    c = conn.cursor()
    now = datetime.datetime.now().isoformat()
    
    # Ingesta en cola de eventos
    macro_headlines = [
        ("MACRO_OIL", "Middle East Oil Exports Rebound as Hormuz Stranglehold Eases"),
        ("MACRO_BONDS", "Sovereign Debt Auctions: US Treasuries, Mexico CETES & Brazil NTN-B Yields Adjust"),
        ("MACRO_INFLATION", "Global CPI & Economic Calendar: Eurozone Inflation Set to Rise, ECB Reports")
    ]
    
    count = 0
    for src, head in macro_headlines:
        c.execute("""
            INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, timestamp)
            VALUES (?, ?, 'PENDING', ?)
        """, (src, head, now))
        if c.rowcount > 0: count += 1

    # Actualización de Métricas de Checklist de Petróleo
    c.execute("""
        INSERT INTO m82_mcn_checklist (timestamp, brent_price, dubai_squeeze, red_day_flag, consecutive_red_days, diesel_shortage_active, real_yield)
        VALUES (?, 107.2, 13.14, 1, 1, 1, 3.30)
    """, (now,))
    
    conn.commit()
    conn.close()
    print(f"📊 [DAEMON MACRO]: Inyectadas {count} señales macro y checklist de petróleo actualizado.")

if __name__ == "__main__":
    run()
PYEOF

# Permisos de ejecución
chmod +x "$DAEMONS_DIR"/*.py

# ----------------------------------------------------
# 4. ORQUESTADOR MAESTRO Y PROCESAMIENTO
# ----------------------------------------------------
echo "⚡ Ejecutando Daemons e Inyectando Telemetría..."
python3 "$DAEMONS_DIR/daemon_refinitiv_world.py"
python3 "$DAEMONS_DIR/daemon_ve_politics.py"
python3 "$DAEMONS_DIR/daemon_macro_yields.py"

echo "🎨 Generando Tarjetas Tácticas HD desde el Motor Unificado..."
python3 "$BASE_DIR/m82_engine_master.py"

echo "=================================================="
echo "✅ DAEMONS INTEGRADOS Y OPERATIVOS EN M82"
echo "=================================================="
