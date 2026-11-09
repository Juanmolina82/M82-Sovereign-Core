# M82 SOVEREIGN CORE :: 10 MESAS QUANTS - DESGLOSE TÉCNICO
Executive Authority: Chairman & CEO Juan M. Molina
Account: jmmp@molina82.com | Molina Holdings LLC
Gobernanza: BUNKER MODE / 0.30x LOCK | Exp 0.22x | VaR 1D 1.68%
Ancla LSEG 6 Nov 16:37 GMT: Brent $97.84 | WTI $90.67 | Spread $7.17
Merey 16: DESVINCULADO $72.00 - $74.50 teórico | Diff -$24.50
WAL: 0/0/0 CLEAN | Censo: 163 (156 Macro + 1 Doctrina + 6 Familia) | 11 RAM

## ARQUITECTURA
- Caracas HQ Central: Gobernanza, asignación Dry Powder
- Charallave L4/L5 Edge: Ingesta 200ms aiohttp, LSEG RDP WebSocket, SQLite WAL
- Supervisor: m82_supervisor.sh bucle 15s
- Persistencia: ~/M82/m82_database.db + ~/M82/sqlite/m82_familia.db
- Presentación: PWA :8080, WSGI :8083, orch.py HUD

## MESA 1 - PE & VC
Foco: Dry Powder $2.008T, Megafondos, European Waterfall 8% Hurdle, 80/20 Carry, 2% GP Skin, Clawback
Scripts: desks/mesa01_pe_vc.py, m82_pe_ingest.py, m82_waterfall.py
RICs: 0#PE=, 0#VC=
Estado: Velación pasiva

## MESA 2 - BANKING & IB
Foco: JPM, BofA, Goldman, Morgan Stanley, SOFR, Curva US10Y
Scripts: desks/mesa02_banking.py, m82_banking_feeder.py
RICs: JPM.N, BAC.N, GS.N, MS.N, US10YT=RR
Estado: Velación pasiva

## MESA 3 - ENERGY & FAJA
Foco: Merey 16 DESVINCULADO, Brent, WTI, Crack Spreads, Faja Orinoco
Scripts: desks/mesa03_energy_faja.py, price_feeder.py, lseg_websocket.py, m82_merey_recalc.py
RICs: LCOc1, CLc1, Merey 16 teórico, 0#VE=
Estado: RECALCULO PASIVO - NO usar $93.15 ITM
Nota: Ancla Brent $97.84. Merey en recálculo $72.00-$74.50 hasta diferencial formal.

## MESA 4 - AEROSPACE & DEFENSE
Foco: RTX, Boeing, SOUTHCOM, Logística
Scripts: desks/mesa04_aero_defense.py
RICs: RTX.N, BA.N
Estado: Velación pasiva

## MESA 5 - AI INFRASTRUCTURE
Foco: ASML High-NA EUV, Nvidia, Clústeres, Regulación AI post-midterms
Scripts: desks/mesa05_ai_infra.py, m82_ai_reg_watch.py
RICs: NVDA.OQ, ASML.OQ
Estado: Velación pasiva - Alerta rout tech por regulación AI

## MESA 6 - CRITICAL MINERALS
Foco: Tierras raras China, Lynas, Litio, Uranio SMR, Cobre LME
Scripts: desks/mesa06_minerals.py
RICs: LYNAS.AX, LME Copper, XAU=
Estado: Velación pasiva

## MESA 7 - SHIPPING & AIS
Foco: Flota CMB.TECH, VLCC, Estrecho Hormuz, UKMTO ataques tanqueros
Scripts: desks/mesa07_shipping_ais.py, m82_ais_tracker.py
RICs: CMB.BR, VLCC rates
Estado: ALERTA ACTIVA - Ataques a ritmo casi récord UKMTO, 1 marino muerto 5 Nov

## MESA 8 - SOVEREIGN DEBT
Foco: Curva US10Y, SOFR, CoCo, VENZ34, PDVSA26, Warsh Spread +102.0 bps
Scripts: desks/mesa08_sov_debt.py
RICs: VENZ34, PDVSA26, US10YT=RR
Estado: Velación pasiva

## MESA 9 - METALS STATS & LME
Foco: Cobre, Oro XAU, Litio, Uranio SMR
Scripts: desks/mesa09_metals_lme.py
RICs: XAU=, LME Copper
Estado: Velación pasiva

## MESA 10 - MACRO & FX
Foco: DXY, Paridades, Canasta OPEP, EMBI Ven, BTC, VIX
Scripts: desks/mesa10_macro_fx.py, m82_fusion_engine.py, m82_verifier.py, m82_kronos_engine.py, m82_agi_quantum_audit.py
RICs: DXY, BTC=, VIX
Estado: Velación pasiva

## CENSO DE INFRAESTRUCTURA M82
- Core Motores: 8 (supervisor, orch, master_dossier, api_server, fusion, agi_quantum, kronos, refinitiv_bridge / price_feeder)
- Mesas Quants: 80 daemons (8+8+8+5+10+8+8+8+8+9)
- Infra / Feeders / Auxiliares: 68 daemons
- Doctrina: 1 daemon (daemon_professional_33.py)
- Familia: 6 daemons (m82_familia.db / 444 Foundation)
- TOTAL SWARM: 163 DAEMONS DEFINIDOS | 11 PROCESOS CORE EN RAM
