import os
import sqlite3
from datetime import datetime

SUPER_DIR = os.path.expanduser("~/M82/super")
SUPER_DB = os.path.join(SUPER_DIR, "m82_super.db")
OUTPUT_HTML = os.path.join(SUPER_DIR, "m82_investor_onepager.html")

def generate_onepager():
    os.makedirs(SUPER_DIR, exist_ok=True)
    
    # Consultar DB Sombra
    legacy_total_bn = 49.3
    stream_id, vol_bpd, annual_bn, corridor, cdd_status = (
        "ZULIA_MEREY16_400K", 400000, 11.68, 
        "USGC (Sweeny / Port Arthur / Lake Charles)", 
        "CITI_NY_ESCROW_ELIGIBLE"
    )

    if os.path.exists(SUPER_DB):
        try:
            conn = sqlite3.connect(SUPER_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(estimated_usd) FROM venezuela_forensic_balance;")
            res = cursor.fetchone()[0]
            if res:
                legacy_total_bn = res / 1e9

            cursor.execute("SELECT stream_id, volume_bpd, annual_gross_usd/1e9, offtake_corridor, cdd_status FROM escrow_cdd_ready LIMIT 1;")
            cdd_row = cursor.fetchone()
            if cdd_row:
                stream_id, vol_bpd, annual_bn, corridor, cdd_status = cdd_row
            conn.close()
        except Exception as e:
            print(f"[!] Warning DB: {e}. Usando valores por defecto de contingencia.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S VET")

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>M82 Executive Investor One-Pager</title>
    <style>
        body {{ font-family: 'Courier New', Courier, monospace; background-color: #0b0f19; color: #d1d5db; padding: 20px; margin: 0; }}
        .container {{ max-width: 900px; margin: auto; border: 1px solid #1f2937; padding: 25px; background-color: #111827; box-shadow: 0 0 15px rgba(0,0,0,0.8); }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 8px; font-size: 18px; text-transform: uppercase; margin-top: 0; }}
        .metric-box {{ display: flex; justify-content: space-between; background: #1e293b; padding: 12px; margin-bottom: 20px; border-left: 4px solid #10b981; }}
        .metric {{ text-align: center; }}
        .metric-title {{ font-size: 10px; color: #9ca3af; text-transform: uppercase; }}
        .metric-value {{ font-size: 15px; font-weight: bold; color: #f3f4f6; margin-top: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 11px; }}
        th, td {{ border: 1px solid #374151; padding: 8px; text-align: left; }}
        th {{ background-color: #1f2937; color: #f9fafb; }}
        .status-tag {{ background-color: #065f46; color: #34d399; padding: 2px 6px; font-size: 10px; font-weight: bold; border-radius: 3px; }}
        .warning-tag {{ background-color: #7f1d1d; color: #fca5a5; padding: 2px 6px; font-size: 10px; font-weight: bold; border-radius: 3px; }}
        .footer {{ border-top: 1px dashed #374151; padding-top: 12px; font-size: 10px; color: #6b7280; text-align: justify; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>M82 Sovereign Intelligence :: Investor Executive Dossier</h1>
        
        <div class="metric-box">
            <div class="metric">
                <div class="metric-title">Bunker Governance</div>
                <div class="metric-value">0.30x LOCK</div>
            </div>
            <div class="metric">
                <div class="metric-title">Exposure / VaR 1D</div>
                <div class="metric-value">0.22x / 1.68%</div>
            </div>
            <div class="metric">
                <div class="metric-title">Warsh Spread</div>
                <div class="metric-value">+102.0 bps</div>
            </div>
            <div class="metric">
                <div class="metric-title">QUBO Optimization</div>
                <div class="metric-value">-15.5000 Energy</div>
            </div>
        </div>

        <h3>1. Balance Forense Histórico (Legacy / Non-Recourse)</h3>
        <table>
            <thead>
                <tr>
                    <th>Activo / Categoría</th>
                    <th>Monto Est. (USD)</th>
                    <th>Estatus Auditoría</th>
                    <th>Custodia Legal</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>RCV Líquidas</td><td>$4.5B</td><td><span class="warning-tag">NO_AUDIT_BIG4</span></td><td>Caracas Bóvedas</td></tr>
                <tr><td>Oro BoE / Fed NY</td><td>$1.8B</td><td><span class="warning-tag">FROZEN_OFAC</span></td><td>Fed NY Custody</td></tr>
                <tr><td>CITGO Equity</td><td>$20.0B</td><td><span class="warning-tag">LITIGATION</span></td><td>OFAC Protected</td></tr>
                <tr><td>Receivables China/Rusia</td><td>$8.0B</td><td><span class="warning-tag">ESTIMATED</span></td><td>Opaque Fleet</td></tr>
                <tr><td>FONDEN / BANDES Legacy</td><td>$15.0B</td><td><span class="warning-tag">OPAQUE</span></td><td>Unauditable</td></tr>
                <tr style="font-weight: bold; background-color: #111827;">
                    <td>TOTAL LEGACY TRAPPED</td>
                    <td>${legacy_total_bn:.1f}B</td>
                    <td colspan="2">Aislado / Fuera de Estructura Escrow</td>
                </tr>
            </tbody>
        </table>

        <h3>2. Pro-Forma Escrow CDD (Flujo Nuevo Bancable)</h3>
        <table>
            <thead>
                <tr>
                    <th>Stream ID</th>
                    <th>Volumen bpd</th>
                    <th>Bruto Anual</th>
                    <th>Corredor Offtake</th>
                    <th>Estatus Citi Escrow</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{stream_id}</td>
                    <td>{vol_bpd:,.0f}</td>
                    <td>${annual_bn:.2f}B / año</td>
                    <td>{corridor}</td>
                    <td><span class="status-tag">{cdd_status}</span></td>
                </tr>
            </tbody>
        </table>

        <div class="footer">
            <p><strong>DECLARACIÓN DE SEGREGACIÓN BANCABLE:</strong> El flujo pro-forma de ${annual_bn:.2f}B/año está completamente aislado de los pasivos históricos y contingencias judiciales de la República ($49.3B). Estructura legal bajo gobernanza legítima Distance 3 (MCM Alpha 0.99).</p>
            <p><strong>Nodo Emisor:</strong> Charallave L4/L5 Edge | <strong>Timestamp:</strong> {timestamp} | <strong>BUNKER STATUS:</strong> SAFE (0.30x LOCK)</p>
        </div>
    </div>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n[✓] ARCHIVO CREADO CON ÉXITO: {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_onepager()
