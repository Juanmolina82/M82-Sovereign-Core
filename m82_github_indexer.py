import os, json, sqlite3, requests, subprocess
from datetime import datetime, timezone

GITHUB_USER = "Juanmolina82"
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
INDEX_PATH = os.path.expanduser("~/M82/github_index")
os.makedirs(INDEX_PATH, exist_ok=True)

print(f"⚡ M82 GITHUB INDEXER (FIXED) — User: {GITHUB_USER}")

# Fetch repos vía GitHub API
repos = []
page = 1
while True:
    try:
        r = requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&page={page}&sort=updated", timeout=20)
        if r.status_code != 200:
            print(f"API Error {r.status_code}: {r.text[:200]}")
            break
        data = r.json()
        if not data:
            break
        repos.extend(data)
        print(f"  Página {page}: {len(data)} repositorios obtenidos")
        if len(data) < 100:
            break
        page += 1
    except Exception as e:
        print(f"Error en consulta API GitHub: {e}")
        break

print(f"✅ Total repositorios obtenidos: {len(repos)}")

# Indexación en SQLite WAL DB
conn = sqlite3.connect(DB_PATH, timeout=60)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=60000;")

conn.execute("""
CREATE TABLE IF NOT EXISTS github_dossier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_name TEXT UNIQUE,
    description TEXT,
    language TEXT,
    stars INTEGER,
    forks INTEGER,
    updated_at TEXT,
    html_url TEXT,
    topics TEXT,
    m82_tag TEXT,
    macro_category TEXT,
    indexed_at TEXT
);
""")

for repo in repos:
    name = repo['name']
    desc = repo.get('description') or ''
    lang = repo.get('language') or 'Unknown'
    stars = repo.get('stargazers_count', 0)
    forks = repo.get('forks_count', 0)
    updated = repo.get('updated_at')
    url = repo.get('html_url')
    topics = ",".join(repo.get('topics', []))

    # Categorización AGI Quantum
    name_low = name.lower()
    if any(k in name_low for k in ['m82', 'trading', 'quant', 'alpha', 'bunker', 'macro']):
        macro_cat = "M82_QUANT_ENGINE"
        tag = "M82_CORE_QUANT"
    elif any(k in name_low for k in ['vla', 'robotics', 'edge', 'jetson', 'orin', 'vision']):
        macro_cat = "ROBOTICS_VLA_EDGE"
        tag = "EDGE_VLA_VALIDATION"
    elif any(k in name_low for k in ['pwa', 'api', 'dashboard', 'stream']):
        macro_cat = "SOVEREIGN_PWA_INFRA"
        tag = "PWA_SOVEREIGN_L4L5"
    elif any(k in name_low for k in ['venezuela', 'vzla', 'mcm', 'petro', 'oil']):
        macro_cat = "VENEZUELA_OIL_SETTHEDATE"
        tag = "SETTHEDATE_VZLA"
    else:
        macro_cat = "GENERAL_TECH_DOSSIER"
        tag = "GITHUB_ROBUST"

    # Registrar en github_dossier
    conn.execute("""
        INSERT OR REPLACE INTO github_dossier (repo_name, description, language, stars, forks, updated_at, html_url, topics, m82_tag, macro_category, indexed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (name, desc, lang, stars, forks, updated, url, topics, tag, macro_cat, datetime.now(timezone.utc).isoformat()))

    # Indexar en macro_dossier
    conn.execute("""
        INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment)
        VALUES (?,?,?,?,?,?)
    """, (f"GITHUB_{GITHUB_USER}", macro_cat, f"{name}: {desc[:120]} | Lang: {lang} | Stars: {stars} | URL: {url} | Topics: {topics}", 0.0, tag, 0.90))

    # Transmitir a m82_multi_stream para reflejo en PWA
    conn.execute("""
        INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, sentiment, asset_impact, event_trigger)
        VALUES (?,?,?,?,?,?,?)
    """, (f"GITHUB_INDEXER_{macro_cat}", f"[GITHUB {GITHUB_USER}] {name} — {desc[:100]} — {lang} — Updated {updated}", "INDEXED_ACTIVE", 0.92, 0.88, "GITHUB_ROBUST", tag))

    print(f"  Indexado: {name} -> {macro_cat} [{tag}]")

conn.commit()

# Resumen
count = conn.execute("SELECT COUNT(*) FROM github_dossier").fetchone()[0]
print(f"✅ GITHUB DOSSIER ROBUSTO — Total indexados: {count}")
conn.close()

# WAL Checkpoint
subprocess.run(["sqlite3", DB_PATH, "PRAGMA wal_checkpoint(TRUNCATE);"])
