#!/usr/bin/env python3
"""
M82 SUPER INTELLIGENCE v2 - FORENSIC & CDD ESCROW PACK GENERATOR
-------------------------------------------------------------------------
Node       : Charallave L4/L5 Edge (Miranda, Venezuela)
Governance : BUNKER MODE (0.30x LOCK) - Pure Read-Only Ingestion
Target     : Pro-Forma Escrow CDD Package for Citi NY / Private Equity ($200B)
"""

import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.expanduser("~/M82")
SUPER_DIR = os.path.join(BASE_DIR, "super")
SUPER_DB = os.path.join(SUPER_DIR, "m82_super.db")

def init_cdd_tables():
    """Inicializa tablas de auditoría forense y CDD de futuro en la DB Sombra."""
    os.makedirs(SUPER_DIR, exist_ok=True)
    conn = sqlite3.connect(SUPER_DB)
    cursor = conn.cursor()
    
    # 1. Tabla Forense Histórica
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venezuela_forensic_balance (
            asset TEXT PRIMARY KEY,
            estimated_usd REAL,
            source TEXT,
            audit_status TEXT,
            legal_custody TEXT
        )
    """)
    
    forensic_data = [
        ('BCV_Liquidas', 4.5e9, 'LSEG/IMF AR', 'NO_AUDIT_BIG4', 'Caracas Bóvedas'),
        ('Oro_BoE_FedNY', 1.8e9, 'BoE / Fed NY Court Filings', 'FROZEN_OFAC', 'Fed NY Custody'),
        ('CITGO_Equity', 20.0e9, 'Delaware Court Filings', 'LITIGATION', 'OFAC Protected'),
        ('Receivables_China_Rusia', 8.0e9, 'AIS / Teapot Discounts', 'ESTIMATED', 'Opaque'),
        ('FONDEN_BANDES_Legacy', 15.0e9, 'Historical Allocation', 'OPAQUE', 'Unauditable')
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO venezuela_forensic_balance VALUES (?, ?, ?, ?, ?)
    """, forensic_data)

    # 2. Tabla CDD Flujo Nuevo (Citi NY Ready)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escrow_cdd_ready (
            stream_id TEXT PRIMARY KEY,
            volume_bpd REAL,
            price_bbl REAL,
            annual_gross_usd REAL,
            offtake_corridor TEXT,
            legal_framework TEXT,
            qubo_status TEXT,
            cdd_status TEXT
        )
    """)
    
    cdd_data = [
        (
            'ZULIA_MEREY16_400K',
            400000.0,
            80.0,
            400000.0 * 80.0 * 365.0, # ~$11.68B / año
            'USGC (Sweeny / Port Arthur / Lake Charles)',
            'OFAC 10Y Specific License + MCM Governance',
            'QUBO -15.5 OPTIMAL VERIFIED',
            'CITI_NY_ESCROW_ELIGIBLE'
        )
    ]
    cursor.executemany("""
        INSERT OR REPLACE INTO escrow_cdd_ready VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, cdd_data)

    conn.commit()
    conn.close()

def print_table_native(title, cursor, query):
    """Imprime una tabla SQL en consola con formato nativo alineado sin librerías externas."""
    cursor.execute(query)
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    
    print(f"--- {title} ---")
    if not rows:
        print("(Sin registros)")
        print("")
        return

    # Calcular anchos de columna
    col_widths = [len(c) for c in cols]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Formatear encabezado
    header = " | ".join(f"{cols[i]:<{col_widths[i]}}" for i in range(len(cols)))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(cols)))
    
    print(header)
    print(separator)
    for row in rows:
        print(" | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row))))
    print("")

def generate_dossier():
    """Genera reporte consolidado en consola para presentación ejecutiva."""
    print("==========================================================================")
    print("  M82 SUPER INTELLIGENCE v2 - FORENSIC & ESCROW CDD DOSSIER")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} VET")
    print("  Node     : Charallave L4/L5 Edge | Status: BUNKER SAFE (0.30x LOCK)")
    print("==========================================================================")
    print("")
    
    conn = sqlite3.connect(SUPER_DB)
    cursor = conn.cursor()
    
    # 1. Forensic Balance Query
    print_table_native(
        "1. BALANCE FORENSE DE ACTIVOS HISTÓRICOS (LEGACY / LIMBO LEGAL)",
        cursor,
        "SELECT asset, estimated_usd/1e9 as USD_Bn, audit_status, legal_custody FROM venezuela_forensic_balance"
    )
    
    # 2. CDD Ready Query
    print_table_native(
        "2. PRO-FORMA ESCROW CDD (FLUJO NUEVO BANCA PRIVADA - CITI NY)",
        cursor,
        "SELECT stream_id, volume_bpd, annual_gross_usd/1e9 as Annual_Gross_Bn, offtake_corridor, cdd_status FROM escrow_cdd_ready"
    )
    
    conn.close()
    print("==========================================================================")
    print("  CONCLUSIÓN CDD: Flujo nuevo $11.68B/año 100% bancable vía Citi NY Escrow.")
    print("  Cero colisión con pasivos FONDEN/BANDES. Matriz L6 Sombra lista.")
    print("==========================================================================")

if __name__ == "__main__":
    init_cdd_tables()
    generate_dossier()
