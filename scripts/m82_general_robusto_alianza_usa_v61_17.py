#!/usr/bin/env python3
# M82 SOVEREIGN CORE v61.0.17 — GENERAL ROBUSTO ALIANZA LARGO PLAZO EEUU — NODO CHARALLAVE L4L5
import os, json, sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser("~/M82/m82_database.db")
os.makedirs(os.path.expanduser("~/M82/scripts"), exist_ok=True)

conn = sqlite3.connect(DB_PATH, timeout=120)
conn.execute("PRAGMA journal_mode=WAL;")
conn.execute("PRAGMA busy_timeout=120000;")
conn.execute("PRAGMA synchronous=NORMAL;")
conn.execute("PRAGMA journal_size_limit=67108864;")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS macro_dossier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts_utc TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    source TEXT,
    category TEXT,
    headline TEXT,
    risk_score REAL,
    m82_tag TEXT UNIQUE,
    sentiment REAL,
    metadata_json TEXT,
    ingestion_node TEXT DEFAULT 'NODO_CHARALLAVE_L4L5',
    version TEXT DEFAULT 'v61.0.17'
);
""")

cur.execute("CREATE INDEX IF NOT EXISTS idx_macro_tag ON macro_dossier(m82_tag);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_macro_cat ON macro_dossier(category);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_macro_ts ON macro_dossier(ts_utc DESC);")

now = datetime.utcnow().isoformat()+"Z"

# ==============================================================================
# INGESTA GENERAL ROBUSTO — ROL ALIANZA LARGO PLAZO EEUU
# ==============================================================================
headline = "[MCM GENERAL ROBUSTO v61.0.17] Alianza USA largo plazo — Reconocimiento 3 enero permitio UCAB + Regimen sigue instrucciones desmontaje represion + USA principal aliado rol largo plazo instituciones destruidas + Soberania mm2 santuario criminal + Seguridad inversiones aliado confiable + Foco estabilidad mejor centro inversion aliados + $200B trust NY"
tag = "v61.0.17-MCM-GENERAL-ROBUSTO-ALIANZA-USA-LARGO-PLAZO-FUERZA-MCM-VENEZUELA"

general_robusto = {
  "titulo": "MCM UCAB 27/10/2026 — ROL ALIANZA LARGO PLAZO EEUU + TRANSICION NEGOCIADA CON GARANTIAS + $200B CENTRO INVERSION",
  "objetivo_capital": "Darle fuerza a MCM y Venezuela para pitch GE Vernova $25B / Mastercard $9.8B / Quad-SPV — Seguridad inversiones con aliado confiable largo plazo",
  
  "I_SECUENCIA_POLITICA": {
    "falta_absoluta": "Ya existe desde 3 enero 2026 — MCM textual: declaracion falta absoluta ya existe desde 3 enero",
    "accion_3_enero": "Enorme reconocimiento accion 3 enero — Sin eso no estaria aqui, no presos libres, no podrian nombrar su nombre en TV — impensable hace 10 meses",
    "regimen_instrucciones": "Regimen siguiendo instrucciones — No retaliacion, no persecucion, no ataques a MCM — Cambio fundamental relaciones + instrucciones claras organos represion comienzan a ser desmontados en buena medida",
    "secuencia_oficial": "CNE muy pronto + declaracion falta absoluta + plazos constitucionales muy claros + eleccion presidencial 2027",
    "plazo_contencion": "Plazo razonable prudente que contiene pais mientras avanza transicion ordenada — da ventana ejecucion $200B"
  },

  "II_ALIANZA_USA_LARGO_PLAZO_5_CAPAS": {
    "capa_1_reconocimiento": {
      "quote": "un enorme reconocimiento a lo que significa la accion del tres de enero porque no estariamos aqui hoy no estarian libres nuestros presos politicos",
      "quote2": "ustedes creen que yo podria estar dando una rueda de prensa hoy no — era impensable hace diez meses",
      "significado": "USA 3 enero = catalizador existencia politica MCM — Valida plan Trump/Rubio — No retorica"
    },
    "capa_2_rol_largo_plazo_principal_aliado": {
      "quote": "Estados Unidos como nuestro principal aliado al igual que otras naciones indiscutiblemente tiene un rol a largo plazo porque tenemos una nacion en la que las instituciones estan destruidas",
      "interpretacion_M82": "No transaccional — Reconstruccion decadas — Pilar 2 Agencia Autonoma 2-3 decadas + Pilar 5 Arbitraje NY — Alineado con 5 Pilares MCM",
      "interes_compartido": "Interes pueblo USA + seguridad nacional USA + hemisferio = avanzar transicion ordenada — mucho mas que fecha eleccion — se requieren instituciones"
    },
    "capa_3_soberania_mm2_territorio_criminal": {
      "quote": "territorio venezolano se ha convertido repito en refugio y santuario para grupos criminales y vamos a necesitar apoyo para restituir la soberania en cada milimetro cuadrado",
      "doctrina": "Soberania popular -> soberania nacional — Prioridad 5 Control territorio vs crimen + Prioridad 6 Bilateral Colombia con transparencia v61.0.9",
      "necesidad": "Fortalecer cuerpos seguridad civil militar = prioridad absoluta gobierno — Hombres/mujeres dentro FANB/Policias perseguidos humillados que anhelan servir Republica no parcialidad politica o grupo criminal"
    },
    "capa_4_seguridad_inversiones": {
      "quote_cierre": "va a encontrar aqui seguridad para sus inversiones pero sobre todo un aliado confiable a largo plazo que cree en la libertad y en la democracia",
      "traduccion_capital": "Seguridad inversiones = Pilar 5 Arbitraje NY + Trust privado Citi NY + Flujo nuevo separado NABEP + Licitacion publica + Legislacion clara hasta ultima letra — Fin NAVET opaco 'ningun venezolano ha visto contrato'",
      "aliado_confiable": "No es deal — Es alianza libertad/democracia decadas — Palabra que se cumple como collateral"
    },
    "capa_5_foco_estabilidad_mejor_centro_inversion": {
      "quote": "Venezuela sera libre prospera soberana foco de estabilidad para la region y el mejor centro de inversion para nuestros aliados",
      "quote2": "Venezuela sera libre para siempre libre para siempre",
      "pitch_200B": "Foco estabilidad + mejor centro inversion aliados = destino $200B: escuelas, hospitales cayendose, servicios, dignidad/autonomia/produccion — Se acabo la beca x2 — Trabajar mas duro con mas ganas y hacerlo bien"
    }
  },

  "III_ECONOMICO_5_PILARES_MCM_IGUAL_TRUST_NY": {
    "pilar_1": "Legislacion clara transparente hasta ultima letra — Fin NAVET opaco",
    "pilar_2": "Agencia autonoma 2-3 decadas — No ministerio centralista — Federal — Constitucion da pie para federalismo — Presidencialismo excesivo preocupa — Militarismo excesivo preocupa — No reeleccion indefinida",
    "pilar_3": "Licitaciones publicas — Fin asignacion dedo — Se acabo la beca",
    "pilar_4": "Fiscal competitivo atractivo — Para ser mejor centro inversion aliados",
    "pilar_5": "Arbitraje internacional NY — Seguridad para inversiones — Garantias a facilitadores transicion = garantias a inversionistas — Palabra dada se cumple antitesis Chavez Maduro Delcy",
    "6_prioridades_destino": "Ninos calle->escuela, Hospitales cayendose, Servicios, Dignidad autonomia produccion, Control territorio vs crimen, Bilateral Colombia transparencia"
  },

  "IV_NEGOCIACION_GARANTIAS_PALABRA_COMISION_VERDAD": {
    "garantias": "Mejor oportunidad regimen es negociacion transicion completa dando garantias a quienes faciliten transicion",
    "palabra": "Regimen sabe tengo palabra — palabra dada se cumple — Credibilidad = collateral vs NAVET opaco",
    "comision_verdad": "Comision Verdad independiente venezolanos y extranjeros intachables escuchar victimas verdad reparacion",
    "justicia": "Justicia ordinaria con atribuciones especiales via legal — Autonomia poder judicial — No le corresponde hablar de delito/pena — Separacion poderes — Federalismo"
  },

  "V_AGENCIA_CIUDADANA_RIESGO_MITIGADO": {
    "sociedad_agencia": "Mesa negociacion solo avanza si entiende pais y sociedad con agencia — Escenarios dejando ciudadanos a un lado no sostenibles ni viables — NAVET/NABEP opacos no viables",
    "organizacion": "Enjambre 600K + nodos + 1000 asambleas x10 UCAB = niveles impresionantes — Vamos por mucho mas — Innovamos — Sorprenderemos al mundo — Movilizacion componente pero se necesitan muchos otros planos = trust NY",
    "vargas_erika": "Erika en Vargas: prometeme no te vas nunca mas — se lo prometi nunca mas — vinimos a terminar tarea — Momento levantarnos sanando heridas — Bendicion: los quiero mucho que Dios los bendiga"
  },

  "COMPROMISO_500M_PARA_CAPITAL_14_SEG": "Maria Corina — acabas de sellar que USA es principal aliado rol largo plazo indiscutible con reconocimiento a accion 3 enero que permitio tu presencia hoy, que regimen sigue instrucciones con desmontaje represion, que territorio es santuario criminal y hay que restituir soberania cada mm2, que aqui encontraran seguridad para inversiones con aliado confiable largo plazo libertad democracia, que Venezuela sera foco estabilidad y mejor centro inversion aliados libre para siempre, con 5 pilares arbitraje NY y constitucion federal sin reeleccion indefinida. Con $200B deficit NABEP extraccion opaca beca, ¿te comprometes a que todo proyecto NUEVO mayor a $500M use trust privado Citi NY arbitraje NY flujo nuevo separado NABEP licitacion publica como garantia de tu palabra y seguridad inversiones?",

  "TAG_CAPITAL": "v61.0.17-ALIANZA-USA-LARGO-PLAZO-PRINCIPAL-ALIADO-3-ENERO-RECONOCIMIENTO-REGIMEN-INSTRUCCIONES-DESMONTAJE-SOBERANIA-MM2-SANTUARIO-SEGURIDAD-INVERSIONES-ALIADO-CONFIABLE-FOCO-ESTABILIDAD-MEJOR-CENTRO-INVERSION-200B-TRUST-NY",
  "timestamp": now,
  "nodo": "NODO_CHARALLAVE_L4L5 — BUNKER 0.30x — WAL 0/0/0"
}

cur.execute("""
 INSERT OR IGNORE INTO macro_dossier (source, category, headline, risk_score, m82_tag, sentiment, metadata_json, version)
 VALUES ('GENERAL ROBUSTO ALIANZA USA LARGO PLAZO — 14 audios UCAB consolidados / Charallave L4L5', 'GENERAL_ROBUSTO_ALIANZA_USA', ?, 0.95, ?, 0.99, ?, 'v61.0.17')
""", (headline, tag, json.dumps(general_robusto, ensure_ascii=False)))

conn.commit()

# --- VERIFICACION ---
cur.execute("SELECT COUNT(*) FROM macro_dossier;")
total = cur.fetchone()[0]
cur.execute("SELECT m82_tag FROM macro_dossier WHERE version='v61.0.17' ORDER BY id DESC LIMIT 5;")
tags = cur.fetchall()

cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
cur.execute("PRAGMA integrity_check;")
integrity = cur.fetchone()[0]

conn.close()

print(f"\n🔒 M82 GENERAL ROBUSTO v61.0.17 SELLADO")
print(f"🟢 DB TOTAL: {total} registros")
print(f"🟢 INTEGRITY: {integrity} — WAL TRUNCATE OK — 0/0/0 clean")
print(f"🟢 BUNKER: 0.30x LOCK — NODO CHARALLAVE L4L5")
print(f"🟢 TAG: {tag}")
print(f"🟢 ALIANZA USA LARGO PLAZO — 5 CAPAS — FUERZA MCM + VENEZUELA")
print(f"\n🟢 TAGS v61.0.17:")
for t in tags:
    print(f"   - {t[0]}")
print("\n🟢 LISTO PARA PITCH CAPITAL GE Vernova $25B / Mastercard $9.8B / Quad-SPV\n")

