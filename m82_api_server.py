#!/usr/bin/env python3
from flask import Flask, request, jsonify
import sqlite3, os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

@app.route('/', methods=['GET', 'POST'])
def analyze():
    from flask import request, jsonify, render_template_string
    import sqlite3, json
    if request.method == 'GET':
        db_path = os.path.expanduser("~/M82/m82_database.db")
        vectores, hjb_meta, top_rows, daemons_cnt = 0, {}, [], 0
        try:
            conn = sqlite3.connect(db_path, timeout=30)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=60000;")
            cur = conn.cursor()
            vectores = cur.execute("SELECT count(*) FROM macro_dossier").fetchone()[0]
            hjb_row = cur.execute("SELECT metadata_json FROM macro_dossier WHERE m82_tag='v60.5-NIVEL-XI-HJB-OPTIMAL-SWITCHING'").fetchone()
            if hjb_row and hjb_row[0]:
                hjb_meta = json.loads(hjb_row[0])
            top_rows = cur.execute("SELECT m82_tag, category, msi_index, risk_score, headline FROM macro_dossier ORDER BY msi_index DESC, id DESC LIMIT 12").fetchall()
            daemons_cnt = cur.execute("SELECT count(*) FROM m82_daemons_registry WHERE status='ACTIVE'").fetchone()[0]
            conn.close()
        except Exception as e:
            top_rows = [("ERROR_DB", "SYSTEM", 0, 0, str(e))]

        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta http-equiv="refresh" content="30">
            <title>M82 Sovereign Core v60.5 | Charallave L4/L5 Edge</title>
            <style>
                body { background:#090d14; color:#e2e8f0; font-family:monospace; margin:0; padding:14px; }
                .hdr { border:1px solid #1e293b; background:#0f172a; padding:12px; border-radius:6px; margin-bottom:12px; }
                .title { color:#38bdf8; font-size:16px; font-weight:bold; }
                .badge { display:inline-block; background:#7f1d1d; color:#fecaca; padding:3px 8px; border-radius:4px; font-size:11px; margin-top:6px; }
                .grid { display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-bottom:12px; }
                .card { background:#0f172a; border:1px solid #1e293b; padding:10px; border-radius:6px; }
                .lbl { color:#94a3b8; font-size:11px; }
                .val { color:#10b981; font-size:16px; font-weight:bold; margin-top:2px; }
                .warn { color:#f59e0b; }
                table { width:100%; border-collapse:collapse; font-size:11px; background:#0f172a; }
                th, td { border:1px solid #1e293b; padding:6px; text-align:left; }
                th { background:#1e293b; color:#38bdf8; }
            </style>
        </head>
        <body>
            <div class="hdr">
                <div class="title">M82 SOVEREIGN CORE v60.5 — CHARALLAVE L4/L5 EDGE</div>
                <div class="badge">BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK | LOCKOUT: NO TRADE</div>
            </div>
            <div class="grid">
                <div class="card"><div class="lbl">EXPOSICIÓN ACTIVA / DRY POWDER</div><div class="val">0.22x / 78.0%</div></div>
                <div class="card"><div class="lbl">VECTORES MACRO DOSSIER</div><div class="val">{{ vectores }} CANÓNICOS</div></div>
                <div class="card"><div class="lbl">RÉGIMEN NIVEL XI (HJB)</div><div class="val warn">{{ hjb_meta.get('regime', 'S1_BUNKER_LOCKOUT') }}</div></div>
                <div class="card"><div class="lbl">WARSH SPREAD / VaR DIARIO</div><div class="val">+102.0 bps / 1.68%</div></div>
            </div>
            <table>
                <tr><th>TAG M82</th><th>MSI</th><th>RISK</th><th>VECTOR INTEL</th></tr>
                {% for r in top_rows %}
                <tr><td>{{ r[0] }}</td><td>{{ r[2] }}</td><td>{{ r[3] }}</td><td>{{ r[4][:90] }}...</td></tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """
        return render_template_string(html, vectores=vectores, hjb_meta=hjb_meta, top_rows=top_rows)

    from flask import request, render_template_string
    import sqlite3, json
    if request.method == "GET":
        db = os.path.expanduser("~/M82/m82_database.db")
        v, hjb, rows = 0, {}, []
        try:
            cn = sqlite3.connect(db, timeout=30)
            cn.execute("PRAGMA journal_mode=WAL;")
            cn.execute("PRAGMA busy_timeout=60000;")
            v = cn.execute("SELECT count(*) FROM macro_dossier").fetchone()[0]
            r = cn.execute("SELECT metadata_json FROM macro_dossier WHERE m82_tag='v60.5-NIVEL-XI-HJB-OPTIMAL-SWITCHING'").fetchone()
            if r and r[0]: hjb = json.loads(r[0])
            rows = cn.execute("SELECT m82_tag, msi_index, risk_score, headline FROM macro_dossier ORDER BY msi_index DESC, id DESC LIMIT 12").fetchall()
            cn.close()
        except Exception as e:
            rows = [("DB_ERR", 0, 0, str(e))]
        tpl = "<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><meta http-equiv=refresh content=30><title>M82 Sovereign Core v60.5</title><style>body{background:#090d14;color:#e2e8f0;font-family:monospace;padding:12px}.box{background:#0f172a;border:1px solid #1e293b;padding:10px;border-radius:6px;margin-bottom:10px}.b{background:#7f1d1d;color:#fecaca;padding:3px 7px;border-radius:4px;font-size:11px;display:inline-block;margin-top:5px}.g{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}.v{color:#10b981;font-size:15px;font-weight:bold}table{width:100%;border-collapse:collapse;font-size:11px;background:#0f172a}th,td{border:1px solid #1e293b;padding:5px;text-align:left}th{background:#1e293b;color:#38bdf8}</style></head><body><div class=box><div style='color:#38bdf8;font-weight:bold'>M82 SOVEREIGN CORE v60.5 | CHARALLAVE L4/L5 EDGE</div><div class=b>BUNKER MODE / CUSTODIA PASIVA 0.30x LOCK | LOCKOUT: NO TRADE</div></div><div class=g><div class=box><div>EXPOSICIÓN / DRY POWDER</div><div class=v>0.22x / 78.0%</div></div><div class=box><div>VECTORES DOSSIER</div><div class=v>{{v}} CANÓNICOS</div></div><div class=box><div>NIVEL XI (HJB)</div><div class=v style='color:#f59e0b'>{{hjb.get('regime','S1_BUNKER_LOCKOUT')}}</div></div><div class=box><div>WARSH SPREAD / VaR</div><div class=v>+102.0 bps / 1.68%</div></div></div><table><tr><th>TAG</th><th>MSI</th><th>RISK</th><th>VECTOR</th></tr>{% for r in rows %}<tr><td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3][:85]}}...</td></tr>{% endfor %}</table></body></html>"
        return render_template_string(tpl, v=v, hjb=hjb, rows=rows)

    data = request.get_json(force=True)
    msg = data.get("message", "").lower()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT source, category, headline, risk_score FROM macro_dosier ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()

    source = row[0] if row else "PE_LARGEST_FUNDS_DESK"
    category = row[1] if row else "MEGA_FUNDS_CONCENTRATION"
    headline = row[2] if row else "Top 10 PE Funds Concentration"
    risk = row[3] if row else 9.8

    hud_image_url = f"http://127.0.0.1:8080/hud_PE_LARGEST_FUNDS_DESK.png"

    response_text = (
        f"=== DESGLOSE EJECUTIVO Y MATRIZ DE IMPACTO M82 ===\n"
        f"🚨 [RISK {risk}] {category}\n"
        f"📌 {headline}\n\n"
        f"![HUD M82]({hud_image_url})\n\n"
        f"• Dry Powder Global: $2.008 Trillones en 1,873 fondos.\n"
        f"• Top 10 Concentración: $189.84B USD (Líder: General Atlantic IV $23.70B).\n"
        f"• Impacto Macro: Capital fuertemente inclinado hacia Megafondos Tech e Infraestructura."
    )

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8083)
