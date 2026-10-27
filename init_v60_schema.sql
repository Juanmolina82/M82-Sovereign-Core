PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- 1. Queue de Ingesta Multicanal
CREATE TABLE IF NOT EXISTS m82_multi_stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_source TEXT,
    headline TEXT UNIQUE,
    status TEXT DEFAULT 'PENDING',
    alpha_score REAL DEFAULT 0.0,
    asset_impact TEXT DEFAULT 'MACRO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Dosier Macro & Telemetría
CREATE TABLE IF NOT EXISTS macro_dossier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT NOT NULL,
    category TEXT DEFAULT 'MACRO',
    headline TEXT NOT NULL,
    risk_score REAL NOT NULL,
    metadata_json TEXT,
    m82_tag TEXT DEFAULT 'M82',
    sentiment REAL DEFAULT 0.0,
    entities TEXT
);

-- 3. Registro y Health Check de Daemons
CREATE TABLE IF NOT EXISTS m82_daemons_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_name TEXT UNIQUE,
    desk_category TEXT,
    vector_type TEXT,
    status TEXT DEFAULT 'ACTIVE',
    last_heartbeat DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Ticks de Precios
CREATE TABLE IF NOT EXISTS price_ticks (
    asset TEXT PRIMARY KEY,
    bid REAL,
    ask REAL,
    last_price REAL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Libro de Órdenes
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stream_id INTEGER,
    asset TEXT,
    side TEXT,
    order_type TEXT DEFAULT 'MARKET',
    qty REAL,
    limit_price REAL,
    fill_price REAL,
    slippage REAL,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Posiciones Cuantitativas
CREATE TABLE IF NOT EXISTS positions (
    asset TEXT PRIMARY KEY,
    current_qty REAL DEFAULT 0.0,
    avg_entry_price REAL DEFAULT 0.0,
    unrealized_pnl REAL DEFAULT 0.0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
