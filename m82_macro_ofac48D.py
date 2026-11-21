import sqlite3, os
from datetime import datetime
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB, timeout=30)
c=conn.cursor()
now=datetime.now().isoformat()
brent, squeeze, fisico = 106.14, 13.14, 119.28

c.executescript("""
CREATE TABLE IF NOT EXISTS m82_ofac_48D (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, licencia TEXT, fecha_ofac TEXT, reemplaza TEXT, que_autoriza TEXT, condiciones TEXT, prohibiciones TEXT, traduccion TEXT);
CREATE TABLE IF NOT EXISTS m82_mcn_checklist (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, brent_price REAL, dubai_squeeze REAL, red_day_flag INTEGER, consecutive_red_days INTEGER, diesel_shortage_active INTEGER, real_yield REAL);
CREATE TABLE IF NOT EXISTS m82_multi_stream (id INTEGER PRIMARY KEY AUTOINCREMENT, daemon_source TEXT, headline TEXT, status TEXT, timestamp TEXT);
CREATE TABLE IF NOT EXISTS m82_ve_deal (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, estructura TEXT, ofac_compliance TEXT);
""")

# OFAC 48D
c.execute("INSERT INTO m82_ofac_48D VALUES (NULL,?,?,?,?,?,?,?,?)", (
now,
"GL 48D - Authorizing the Supply of Certain Items and Services to Venezuela",
"2026-09-28 - junto con 46E y 49B",
"48C del 27 agosto 2026",
"US persons suministrar bienes, tecnologia, servicios para petroleo, gas, petroquimica incluye fertilizantes y electricidad, incluso con Gobierno y PDVSA - mantener y operar",
"Arbitraje US, UK, Francia, Singapur - Pagos a personas bloqueadas salvo impuestos/tasas locales van a cuentas Tesoro US bajo EO 14373 no al regimen - Reporte obligatorio a Estado y Energia",
"NO: China,Rusia,Iran,Cuba,Corea del Norte - NO diluyentes (GL47B separado) - NO nuevas JV/entidades - NO pagos oro/petro/cripto Gobierno - NO desbloquear bienes - NO buques sancionados - Ley US debe gobernar contrato",
"Se puede mantener y operar. No se puede entregar el control ni el dinero."
))

# Checklist
c.execute("INSERT INTO m82_mcn_checklist VALUES (NULL,?,?,?,?,?,?,?)", (now, brent, squeeze, 1, 1, 1, 3.0))

# Update VE DEAL con compliance OFAC
c.execute("INSERT INTO m82_ve_deal (timestamp, estructura, ofac_compliance) VALUES (?,?,?)", (
now,
"Betancourt/Sargent 17 campos redibujados 160-200k bpd 170k/350k max 35% equity penny warrants $0.01 OSC Pentagon + 20% at cost triangulacion JP8 - 1T in situ 20% Chavez vs 5-8% real M82_MACRO fake - narrativa electoral tipo Ucrania",
"OFAC 48D COMPLIANCE: 1) No nueva JV -> por eso redibujo campos existentes 2) Penny warrants $0.01 = derecho no propiedad hasta ejercer -> no es entrega control 3) 20% at cost pago a cuenta Tesoro EO14373 no regimen 4) Arbitraje US/UK/Francia/Singapur 5) Sin diluyentes/China/Rusia/Iran/Cuba/NK - Reporte Estado/Energia - Estructura calza perfecto GL 48D + GL49B contingent contracts"
))

heads=[
f"{now} | OFAC 48D HOY 28/09/2026: Autoriza US persons bienes/tecnologia/servicios petroleo gas petroquimica fertilizantes electricidad incluso con Gobierno y PDVSA - Reemplaza 48C 27ago - Junto 46E y 49B",
f"{now} | OFAC CONDICIONES: Arbitraje US/UK/Francia/Singapur - Pagos bloqueados -> cuentas Tesoro US EO14373 no regimen salvo impuestos/tasas locales - Reporte Estado y Energia obligatorio",
f"{now} | OFAC PROHIBIDO: China Rusia Iran Cuba Corea Norte - diluyentes - nuevas JV - oro/petro/cripto Gobierno - desbloquear bienes - buques sancionados",
f"{now} | TRADUCCION M82: Se puede mantener y operar No se puede entregar control ni dinero - Por eso 35% penny warrants + 20% at cost a Tesoro US + 17 campos redibujados no JV nueva",
f"{now} | M82 FINAL V6 OFAC: Fisico {fisico} (106.14+13.14) Perdida {fisico+40:.2f} vs -40 | Deal calza GL48D/49B | Reservas 20% vs 5-8% M82_MACRO fake | Impacto 0 Brent | Riesgo sube | Electoral Ucrania",
]

for h in heads:
    c.execute("INSERT INTO m82_multi_stream VALUES (NULL,?,?,?,?)", ("M82_OFAC_48D_V6", h, "PENDING", now))

conn.commit()
conn.close()
print(f"✅ V6 OFAC 48D OK Fisico {fisico}")
