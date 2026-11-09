#!/usr/bin/env python3
import sqlite3, os, json
from datetime import datetime
DB_PATH = os.path.expanduser("~/M82/m82_database.db")
conn = sqlite3.connect(DB_PATH, timeout=120)
conn.execute("PRAGMA journal_mode=WAL;")
cur = conn.cursor()
now = datetime.utcnow().isoformat()+"Z"

headline = "[MCM GENERAL CAPITAL] Secuencia CNE falta absoluta 3 enero eleccion 2027 + Regimen instrucciones desmontaje + USA aliado largo plazo seguridad mm2 + 5 Pilares arbitraje NY seguridad inversiones + Federal no reeleccion + $200B foco estabilidad mejor centro inversion aliado confiable + Se acabo beca"
tag = "v61.0.16-MCM-GENERAL-CAPITAL-ECONOMICO-USA-200B-FOCO-ESTABILIDAD"

meta = {
 "general_capital": {
  "secuencia": "CNE muy pronto + falta absoluta ya existe 3 enero + eleccion 2027 + plazos constitucionales claros",
  "regimen": "Sigue instrucciones - no retaliacion - desmontaje organos represion buena medida - cambio fundamental relaciones",
  "usa": "Reconocimiento enorme accion 3 enero - sin eso no rueda prensa UCAB ni presos libres - principal aliado rol largo plazo indiscutible - interes seguridad nacional USA - apoyo restituir soberania cada mm2 - territorio santuario criminal",
  "5_pilares": "1 Legislacion clara 2 Agencia autonoma decadas 3 Licitaciones 4 Fiscal competitivo 5 Arbitraje NY = seguridad inversiones",
  "6_prioridades": "Ninos escuela hospitales servicios dignidad territorio crimen bilateral Colombia",
  "constitucion": "Federal - presidencialismo excesivo preocupa - militarismo excesivo - no reeleccion indefinida - Punto Acuerdo millones opiniones reforma/nueva constitucion",
  "negociacion": "Mejor oportunidad regimen negociacion con garantias facilitadores - palabra dada se cumple - antitesis Chavez Maduro Delcy - Comision Verdad independiente - Justicia ordinaria tribunales especiales - Autonomia judicial",
  "agencia": "Sociedad con agencia - escenarios sin ciudadanos no sostenibles - NAVET opaco no viable - Organizacion impresionante 600K + sorpresa mundial",
  "cierre_capital": "Seguridad para sus inversiones + Aliado confiable largo plazo libertad democracia + Se acabo beca x2 + Trabajar mas duro bien + Libre prospera soberana foco estabilidad mejor centro inversion aliados + Libre para siempre x2 + Bendicion",
  "compromiso_500M": "Todo proyecto NUEVO >$500M trust privado Citi NY arbitraje NY flujo nuevo separado NABEP licitacion publica - federalismo financiero"
 },
 "timestamp": now
}

cur.execute("INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json) VALUES ('GENERAL CAPITAL CONSOLIDADO UCAB 14 audios / Charallave L4L5', 'GENERAL_CAPITAL', ?, 1.0, ?, 0.99, ?)", (headline, tag, json.dumps(meta, ensure_ascii=False)))
conn.commit()
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
print(f"GENERAL CAPITAL SELLADO — TOTAL {cur.fetchone()[0]} — {tag}")
conn.close()
