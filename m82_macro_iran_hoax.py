import sqlite3, os
from datetime import datetime
DB=os.path.expanduser("~/M82/m82_database.db")
conn=sqlite3.connect(DB, timeout=30)
c=conn.cursor()
now=datetime.now().isoformat()

brent, wti, squeeze = 107.2, 94.1, 13.1
fisico = brent + 12.5 # Dubai physical premium

c.execute("INSERT INTO m82_mcn_checklist (timestamp, brent_price, dubai_squeeze, red_day_flag, consecutive_red_days, diesel_shortage_active, real_yield) VALUES (?,?,?,?,?,?,?)",
(now, brent, squeeze, 1, 2, 1, 3.30))

for f,e,p,i,est,br in [
("2026-09-28 16:21 EDT","Trump denies Iran sanctions relief Axios hoax","US/IR","CRITICO","Trump denies Axios relief report = hoax - Mantiene sanciones Iran - no vuelve crudo irani - Bullish Brent >107 WTI >94 - Strait Hormuz cerrado",brent),
("2026-09-28","Brent +3% >107 after reject 7-day truce","GLOBAL","CRITICO","Reject truce = oil soaring war fears grow - Iran queria lift blockade + lift oil sanctions + frozen assets + regional ceasefire - Trump: overplayed hand - not deal I want",brent),
("2026-09-28","WTI 92.96->94.1 +0.6% to +3% - Squeeze validado","US","ALTO",f"WTI {wti} Brent {brent} spread {squeeze} - Hormuz 20M bpd transito max desde conflicto - but naval blockade sigue",brent),
]:
    c.execute("INSERT INTO m82_calendario_macro (fecha,evento,pais,impacto,estado,brent_ref) VALUES (?,?,?,?,?,?)",(f,e,p,i,est,br))

for pt in [-40.0, -54.65]:
    c.execute("INSERT INTO m82_perdida_audit VALUES (NULL,?,?,?,?,?,?,?)",(now, brent, squeeze, brent+squeeze, pt, (brent+squeeze)-pt, 1))

c.execute("INSERT INTO m82_ofac_48D (timestamp, licencia, fecha_ofac, reemplaza, que_autoriza, condiciones, prohibiciones, traduccion) VALUES (?,?,?,?,?,?,?,?)",(
now,
"GL48D + Iran hoax denial",
"2026-09-28",
"Axios report sanctions relief = hoax",
"Iran sanctions siguen - no relief sin nuclear concrete progress - OFAC VE 48D autoriza operar VE pero no entregar control/dinero",
"VE: pagos a Tesoro EO14373 arbitraje US/UK/Francia/Singapur - IRAN: no lift oil sanctions sin nuclear commitments",
"IRAN: no frozen assets release no oil sales lift - VE: no China/Rusia/Iran/Cuba/NK no diluyentes no nueva JV no oro/petro/cripto",
"Bullish Brent: Iran crudo no vuelve + VE 170k/350k no mueve mercado + Hormuz riesgo = squeeze 13+ se mantiene"
))

heads=[
f"{now} | IRAN HOAX: Trump denies Axios Iran sanctions relief = hoax - Mantiene sanciones - Bullish oil Brent {brent} +3% >107 WTI {wti} >94 - Iran overplayed hand",
f"{now} | TRUCE REJECT: Brent jumped 3% Monday after Trump rejected 7-day truce Hormuz - Iran queria lift naval blockade + oil sanctions + frozen assets - Trump: not deal I want",
f"{now} | OFAC vs IRAN: VE GL48D permite operar 35%+20% at cost a Tesoro no regimen - IRAN no relief sin nuclear progress - Strait Hormuz 20M bpd pero blockade sigue - squeeze {squeeze}",
f"{now} | PERDIDA UPDATE: Brent {brent}+{squeeze}={brent+squeeze} vs -40 = {brent+squeeze+40:.2f} perdida - Red Day 2/90 Real Yield 3.30% 10Y 5.232% 30Y 5.55%",
]

for h in heads:
    c.execute("INSERT INTO m82_multi_stream VALUES (NULL,?,?,?,?)", ("M82_IRAN_HOAX_V8", h, "PENDING", now))

conn.commit()
conn.close()
print(f"✅ V8 IRAN HOAX OK Brent {brent} WTI {wti}")
