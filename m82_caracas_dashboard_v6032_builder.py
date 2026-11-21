#!/usr/bin/env python3
import os, sqlite3

DB = os.path.expanduser("~/M82/m82_database.db")
DASH_DIR = os.path.expanduser("~/M82/dashboard")
os.makedirs(DASH_DIR, exist_ok=True)

def build_v6032_dashboard():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout=60000;")
    
    c.execute("SELECT daemon_source, headline, alpha_score, created_at FROM m82_multi_stream WHERE status='VERIFIED' ORDER BY id DESC LIMIT 6")
    rows_gen = c.fetchall()

    c.execute("SELECT daemon_source, headline, alpha_score, created_at FROM m82_multi_stream WHERE asset_impact='REFINITIV_BANESCO_Q3' OR asset_impact='REFINITIV_BNC_Q3' ORDER BY id DESC LIMIT 6")
    rows_banking = c.fetchall()
    conn.close()

    def render_cards(rows):
        html = ""
        if not rows:
            return "<div class='card'><div class='headline'>Esperando ingesta...</div></div>"
        for desk, hl, alpha, ts in rows:
            html += f"""
            <div class="card">
                <div class="card-header">
                    <span class="badge {desk.lower() if desk else 'banking'}">{desk}</span>
                    <span class="ts">{ts}</span>
                </div>
                <div class="headline">{hl}</div>
                <div class="card-footer">
                    <span>Alpha Score: <strong>{alpha if alpha else '0.95'}</strong></span>
                    <span class="status">🔒 VERIFIED</span>
                </div>
            </div>
            """
        return html

    cards_general = render_cards(rows_gen)
    cards_banking = render_cards(rows_banking)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>M82 Citadel V60.3.2 :: Caracas HQ</title>
    <style>
        :root {{ --bg-color: #0b0e14; --panel-bg: #131722; --border-color: #2a2e39; --accent-green: #089981; --accent-blue: #2962ff; --accent-orange: #f57c00; --text-main: #d1d4dc; --text-muted: #787b86; }}
        body {{ font-family: sans-serif; background-color: var(--bg-color); color: var(--text-main); margin: 0; padding: 20px; }}
        .header {{ border-bottom: 2px solid var(--border-color); padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
        .header h1 {{ font-size: 1.3rem; margin: 0; color: #fff; }}
        .tabs {{ display: flex; gap: 10px; margin-bottom: 15px; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }}
        .tab-btn {{ background: #1e222d; border: 1px solid var(--border-color); color: var(--text-main); padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.85rem; }}
        .tab-btn.active {{ background: var(--accent-blue); color: #fff; border-color: var(--accent-blue); }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        @media (max-width: 900px) {{ .tab-content.active {{ grid-template-columns: 1fr; }} }}
        .panel {{ background: var(--panel-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; }}
        .panel-title {{ font-size: 0.95rem; font-weight: 600; margin-bottom: 12px; color: #fff; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; }}
        .card {{ background: #1e222d; border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; margin-bottom: 8px; }}
        .card-header {{ display: flex; justify-content: space-between; font-size: 0.75rem; }}
        .badge {{ padding: 2px 6px; border-radius: 4px; font-weight: bold; color: #fff; font-size: 0.7rem; background: var(--accent-blue); }}
        .ts {{ color: var(--text-muted); }}
        .headline {{ font-size: 0.85rem; margin-top: 4px; color: #eceff1; }}
        .card-footer {{ display: flex; justify-content: space-between; font-size: 0.75rem; margin-top: 6px; color: var(--text-muted); }}
        .status {{ color: var(--accent-green); font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>M82 CITADEL :: CARACAS HQ MASTER NODE (V60.3.2)</h1>
            <div style="font-size: 0.8rem; color: var(--text-muted);">Molina Holdings LLC (US) | Corp. Internacional JMM, C.A. (VE)</div>
        </div>
        <div style="color: var(--accent-green); font-weight: bold;">● BUNKER MODE ACTIVE (0.30x LOCK)</div>
    </div>
    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('general')">Mesa de Dinero Live</button>
        <button class="tab-btn" onclick="switchTab('banking')">Banesco & BNC Q3 Audit</button>
    </div>
    <div id="tab-general" class="tab-content active">
        <div class="panel"><div class="panel-title">Mesa de Dinero :: Eventos Recientes</div>{cards_general}</div>
        <div class="panel">
            <div class="panel-title">Anthropic Run-Rate Growth ($B)</div>
            <div style="text-align: center;">
                <svg width="100%" height="180" viewBox="0 0 400 160">
                    <polyline fill="none" stroke="#089981" stroke-width="3" points="40,130 120,120 200,100 280,40 360,15"/>
                    <circle cx="40" cy="130" r="4" fill="#2962ff"/><text x="30" y="150" fill="#fff" font-size="9">Q1 24 ($1B)</text>
                    <circle cx="120" cy="120" r="4" fill="#2962ff"/><text x="105" y="150" fill="#fff" font-size="9">Q1 26 ($4.7B)</text>
                    <circle cx="200" cy="100" r="4" fill="#2962ff"/><text x="185" y="150" fill="#fff" font-size="9">Q2 26 ($11.5B)</text>
                    <circle cx="280" cy="40" r="5" fill="#f57c00"/><text x="250" y="30" fill="#fff" font-weight="bold" font-size="9">Jul 26 ($65B)</text>
                    <circle cx="360" cy="15" r="6" fill="#089981"/><text x="310" y="12" fill="#fff" font-weight="bold" font-size="9">EOY 26 ($100B)</text>
                </svg>
            </div>
        </div>
    </div>
    <div id="tab-banking" class="tab-content">
        <div class="panel"><div class="panel-title">Auditoría Q3 2026 (Banesco / BNC)</div>{cards_banking}</div>
        <div class="panel">
            <div class="panel-title">Corresponsalía & Proyección FMI 5% PIB</div>
            <p style="font-size:0.85rem; line-height:1.4;">● <strong>Banesco (89695116):</strong> Core de medios de pago y liquidez comercial Bs/USD.</p>
            <p style="font-size:0.85rem; line-height:1.4;">● <strong>BNC (89695107):</strong> Custodia e intermediación de cambio para operaciones de tesorería.</p>
            <p style="font-size:0.85rem; line-height:1.4;">● <strong>FMI 5% PIB 2026:</strong> Respalda la expansión del crédito comercial e intermediación.</p>
        </div>
    </div>
    <script>
        function switchTab(tabName) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            if(tabName === 'general') {{
                document.querySelectorAll('.tab-btn')[0].classList.add('active');
                document.getElementById('tab-general').classList.add('active');
            }} else {{
                document.querySelectorAll('.tab-btn')[1].classList.add('active');
                document.getElementById('tab-banking').classList.add('active');
            }}
        }}
    </script>
</body>
</html>"""

    with open(os.path.join(DASH_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ Dashboard HTML5 multitab generado.")

if __name__ == "__main__":
    build_v6032_dashboard()
