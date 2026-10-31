import sqlite3, os
from datetime import datetime
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB, timeout=30)
c=conn.cursor()
now=datetime.now().isoformat()

# Tabla reservas audit
c.execute("""CREATE TABLE IF NOT EXISTS m82_reservas_audit (
id INTEGER PRIMARY KEY AUTOINCREMENT,
timestamp TEXT, recurso_in_situ TEXT, factor_chavez TEXT, factor_real TEXT,
costo_metodo TEXT, concepto_sec TEXT, fuente TEXT, impacto_deal TEXT
)""")

c.execute("INSERT INTO m82_reservas_audit VALUES (NULL,?,?,?,?,?,?,?,?)", (
now,
"1 trillon (1 billon ES) barriles en sitio Faja del Orinoco - OPESPI 300 MMM viene de aqui",
"20% ordenado por Chavez para ser reserva #1 mundial",
"5-8% real con metodos convencionales historico VE",
"Canadiense SAGD: calentar yacimiento + inyeccion vapor - costos altisimos - nunca hecho a escala VE - ninguna empresa incentivo",
"Recurso != Reserva probada M82_MACRO: necesita viabilidad economica + tecnica. Si listara en NYSE, reduccion dramatica",
"Francisco Audio4 - critica por cifra OPESPI",
"17 campos redibujados incluyen greenfields Guárico con recurso no viable - sobrevaluacion $300M buyout Sargent - deal 35%+20% basado en reservas infladas"
))

# Update deal VE con nota reservas
c.execute("UPDATE m82_ve_deal SET campos = campos || ' | RESERVAS INFLADAS: 1 trillon in situ pero 5-8% real vs 20% Chavez - M82_MACRO no lo aceptaria como probada' WHERE id = (SELECT MAX(id) FROM m82_ve_deal)")

headlines = [
f"{now} | AUDIO4 RESERVAS FAKE: OPESPI 300MMM es calculo estimado Chavez 20% recobro ordenado a PDVSA para ser #1 mundial - Real 5-8% convencional",
f"{now} | FAJA 1 TRILLON in situ pero solo fraccion recuperable - Metodo canadiense vapor SAGD costos altisimos nunca hecho escala VE - sin incentivo",
f"{now} | M82_MACRO RULES: Recurso != Reserva probada - Necesita viabilidad economica+tecnica - Si lista en NYSE EEUU reduccion dramatica - Criticas Francisco por esto",
f"{now} | IMPACTO DEAL: 17 campos redibujados con greenfields Guarico basados en cifra inflada 20% - Valor real 35% equity $300M sobrevaluado - Triangulacion JP8 no cambia",
]

for h in headlines:
    c.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp) VALUES (?,?,?,?)", ("M82_AUDIO4_RESERVAS_FAKE", h, "PENDING", now))
    c.execute("INSERT INTO m82_calendario_macro (fecha, evento, pais, impacto, estado, brent_ref) VALUES (?,?,?,?,?,?)",
              ("2026-09-28", "Audio4 Reservas Faja 20% vs 5-8% M82_MACRO", "VE", "CRITICO", "OPESPI 300MMM inflado por Chavez - 1 trillon in situ pero 5-8% real - SAGD canadiense nunca hecho VE", 106.14))

conn.commit()
conn.close()
print("✅ Audio4 reservas fake inyectado - core final completo")
