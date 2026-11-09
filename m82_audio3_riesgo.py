import sqlite3, os
from datetime import datetime
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB, timeout=30)
c=conn.cursor()
now=datetime.now().isoformat()

# Nueva tabla de tesis riesgo
c.execute("""CREATE TABLE IF NOT EXISTS m82_riesgo_politico (
id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, produccion_adicional TEXT, impacto_precio TEXT, estabilidad_tesis TEXT, riesgo_eval TEXT, fuente TEXT
)""")

c.execute("INSERT INTO m82_riesgo_politico VALUES (NULL,?,?,?,?,?,?)", (
now,
"2026: 170k bpd optimista oficial / 2027: 350k bpd max con Chevron + deal nuevo",
"No impacto Brent 106.14 / gasolina US - 10M disrupcion global - Guyana/Brasil/Argentina agregan mas que VE",
"Inversion gran escala necesita capital enorme + largo plazo + estabilidad democratica + Estado Derecho + electoral",
"Deal opaco, no cuadra sistema legal VE, negociacion asimetrica, empresas no majors, US equity garantiza propiedad pero INCREMENTA riesgo politico para resto - oportunidad perdida",
"Francisco Audio3 - antes Noviembre - Trump"
))

# Update m82_ve_deal con evaluacion
c.execute("UPDATE m82_ve_deal SET spr_logica = spr_logica || ' | AUDIO3: No mueve precio - 170k/350k vs 10M global - timing antes Nov' WHERE id = (SELECT MAX(id) FROM m82_ve_deal)")

# Headlines para orquestador
headlines = [
f"{now} | AUDIO3 FRANCISCO CRITICO: 170k bpd 2026 + 350k bpd max 2027 con Chevron - vs 10M disrupcion - NO IMPACTO BRENT 106.14 ni gasolina US - Guyana/Brasil/Argentina > VE",
f"{now} | TESIS ROTA: Inversion gran escala necesita estabilidad democratica / Estado Derecho / electoral - US no eligio via politica sino salida opaca",
f"{now} | RIESGO POLITICO SUBE: US equity garantiza propiedad para inversionistas deal y hace dificil renegociar, pero negociacion asimetrica + no cuadra legal VE + empresas no establecidas = INCREMENTA riesgo resto mercado - oportunidad perdida",
f"{now} | TIMING: Acuerdo manana/pasado - antes Noviembre expectativa Trump - cierre expedito"
]

for h in headlines:
    c.execute("INSERT INTO m82_multi_stream (daemon_source, headline, status, timestamp) VALUES (?,?,?,?)", ("M82_AUDIO3_RIESGO_VE", h, "PENDING", now))

conn.commit()
conn.close()
print("✅ Audio3 riesgo politico inyectado")
