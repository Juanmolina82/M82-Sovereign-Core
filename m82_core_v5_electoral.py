import sqlite3, os
from datetime import datetime
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB, timeout=30)
c=conn.cursor()
now=datetime.datetime.now().isoformat()

c.execute("""CREATE TABLE IF NOT EXISTS m82_narrativa_electoral (
id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, claim TEXT, realidad TEXT, precedente TEXT, impacto_m82 TEXT
)""")

c.execute("INSERT INTO m82_narrativa_electoral VALUES (NULL,?,?,?,?,?)", (
now,
"Empresa privada con reservas más altas del mundo entre privados - colosal - 300MM OPESPI - 1 trillon in situ",
"Estimado no extraible en 25 años - 5-8% real vs 20% Chavez - recurso != reserva M82_MACRO - SAGD canadiense nunca hecho VE",
"Acuerdo minerales Ucrania US - anuncio rimbombante electoral, firma, pero en practica no ha pasado nada",
"V5: 35% equity penny warrants + 20% at cost $300M 170k/350k bpd no mueve Brent 106.14+13.14=119.28 - triangulacion JP8 - riesgo politico sube - narrativa electoral noviembre Trump"
))

# Update reservas audit con electoral
c.execute("UPDATE m82_reservas_audit SET impacto_deal = impacto_deal || ' | AUDIO5: Claim electoral reservas privadas mas altas mundo = marketing, no extraible 25 años, como Ucrania minerales - anuncio rimbombante sin ejecucion' WHERE id = (SELECT MAX(id) FROM m82_reservas_audit)")

headlines = [
f"{now} | AUDIO5 CIERRE: Es estimado gigantesco pero en 25 anos no vas a poder sacar - claim empresa privada reservas mas altas mundo = colosal marketing electoral",
f"{now} | PRECEDENTE UCRANIA: Anuncio minerales rimbombante firma acuerdo pero practica no ha pasado nada - mismo patron VE 35%+20% antes noviembre",
f"{now} | M82 V5 FINAL: Brent 106.14 + 13.14 = 119.28 fisico | Perdida -$40 = 159.28 | Deal 35% penny warrants $300M 170k/350k bpd no mueve mercado | Reservas 20% Chavez vs 5-8% real M82_MACRO fake | Riesgo politico sube | Narrativa electoral",
]

for h in headlines:
    c.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp) VALUES (?,?,?,?)", ("M82_AUDIO5_ELECTORAL_FINAL", h, "PENDING", now))

conn.commit()
conn.close()
print("✅ V5 electoral final inyectado")
