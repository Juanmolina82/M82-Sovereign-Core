#!/usr/bin/env python3
from flask import Flask, request, jsonify
import sqlite3, os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.expanduser("~/M82")
DB_PATH = os.path.join(BASE_DIR, "m82_database.db")

@app.route('/', methods=['POST'])
def analyze():
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
