import sqlite3
import json

def ingest_signal(source, category, asset_class, risk_score, headline, payload_dict=None):
    """
    Inyecta una señal en m82_database.db respetando el esquema real de la tabla.
    Si se pasa un payload_dict, se anexa al headline para mantener la trazabilidad.
    """
    conn = sqlite3.connect("m82_database.db")
    cursor = conn.cursor()

    # Si hay un payload estructural, aseguramos que la información clave quede visible en el headline o logs
    full_headline = headline
    if payload_dict and "structure_notes" in payload_dict:
        full_headline += f" | {payload_dict['structure_notes']}"

    cursor.execute("""
    INSERT INTO signals (source, category, asset_class, risk_score, headline, timestamp)
    VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (source, category, asset_class, risk_score, full_headline))

    conn.commit()
    conn.close()
    print(f"✅ Señal inyectada con éxito: [{category}] {headline[:45]}... (Risk: {risk_score})")

if __name__ == "__main__":
    # Ejemplo de uso / Test rápido
    print("Módulo de ingesta M82 listo.")
