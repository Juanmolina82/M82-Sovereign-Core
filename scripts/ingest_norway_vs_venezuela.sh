#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

CREATE TABLE IF NOT EXISTS historical_contract_dossier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period TEXT NOT NULL,
    country TEXT NOT NULL,
    contract_model TEXT NOT NULL,
    royalty_fiscality TEXT NOT NULL,
    custody_governance TEXT NOT NULL,
    rent_destination TEXT NOT NULL,
    ingestion_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Inserción Período 1890-1935
INSERT INTO historical_contract_dossier (period, country, contract_model, royalty_fiscality, custody_governance, rent_destination)
VALUES 
('1890-1935', 'Venezuela', 'Concesión Feudal (40-50 años)', '10%-15% Regalía, Sin ISRR', 'Custodia Centralizada (Tesorería)', 'Gasto Corriente e Infraestructura Básica'),
('1890-1935', 'Noruega', 'N/A (Pre-Descubrimiento)', 'N/A', 'N/A', 'N/A');

-- Inserción Período 1936-1975
INSERT INTO historical_contract_dossier (period, country, contract_model, royalty_fiscality, custody_governance, rent_destination)
VALUES 
('1936-1975', 'Venezuela', 'Concesiones 50/50 / Ley 1943', '16.66%-50% ISRR', 'Presupuesto Nacional Directo (Sin separación)', 'Consumo e Infraestructura; Sin Regla Fiscal'),
('1936-1975', 'Noruega', 'Concesión Statoil / Ekofisk 1969', 'Regalía Progresiva + 78% Tax', 'Separación Regulador / Statoil', 'Desarrollo de Know-How Offshore / Infraestructura');

-- Inserción Período 1976-1998
INSERT INTO historical_contract_dossier (period, country, contract_model, royalty_fiscality, custody_governance, rent_destination)
VALUES 
('1976-1998', 'Venezuela', 'Nacionalización / Apertura Petrolera', '1%-16.66% Regalía (Apertura)', 'FIEM 1998 (Vaciado por BCV / Sin blindaje)', 'Financiamiento de Céficit Fiscal'),
('1976-1998', 'Noruega', 'Government Petroleum Fund (1990)', '78% Marginal Tax Rate', 'Norges Bank Investment Management (NBIM)', 'Preservación de Capital / Regla Fiscal del 3%');

-- Inserción Período 1999-2026
INSERT INTO historical_contract_dossier (period, country, contract_model, royalty_fiscality, custody_governance, rent_destination)
VALUES 
('1999-2026', 'Venezuela', 'Empresa Mixta Forzada (60% PDVSA)', '33% Regalía + 50% Extracción (16% WACC Opaco)', 'BCV / FONDEN / Cuentas Opacas ($150B Claims)', 'Gasto Social Directo / Colapso de Producción'),
('1999-2026', 'Noruega', 'Equinor / GPFG Sovereign Fund', '78% Tax + Carbon Credits', 'Custodia Offshore Global (NBIM)', 'Fondo Soberano ($1.7T+ / $1.4M por ciudadano)');

-- Inserción M82 Quad-SPV Solution
INSERT INTO historical_contract_dossier (period, country, contract_model, royalty_fiscality, custody_governance, rent_destination)
VALUES 
('2026+', 'M82 Quad-SPV (Venezuela Solution)', 'Ring-Fenced Quad-SPV (EU/US/SG/AU)', '9.95% Blended WACC / ESG Cleansed Heavy', 'Master Escrow Citibank NY / Euroclear / CIADI', 'Waterfall Auditado LSEG: Deuda -> SAGD Capex -> Dividendo');

-- Registro en Macro Dossier
INSERT OR REPLACE INTO macro_dossier (topic, summary, risk_score, source)
VALUES (
    'NORWAY_VS_VENEZUELA_CONTRACT_DOSSIER',
    '100-Year Contractual Timeline Analysis. Venezuela failed due to internal custody in BCV/FONDEN without fiscal rules. M82 Quad-SPV replicates Norway model via offshore trustees (Citi NY/Euroclear), 9.95% WACC, and CIADI/UNCITRAL governance.',
    9.8,
    'CHAIRMAN_DIRECTIVE_M2'
);

EOF_SQL

echo "✅ Historical Dossier & Norway Parallel Ingested Successfully into SQLite3 WAL Database."
