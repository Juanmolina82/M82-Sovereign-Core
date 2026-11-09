# M82 QUANTUM MACRO DOSSIER — SYSTEM ARCHITECTURE & ORGANIZATION

## 🏢 Jerarquía de Sedes Institucionales

### Nivel 1: Sede Central Principal (HQ)
* **Ubicación:** Caracas, Venezuela
* **Rol:** Command & Control / Gobernanza Global / Toma de Decisiones
* **Responsabilidades:**
  * Consolidación y visualización de métricas ejecutivas.
  * Punto central de publicación PWA Master.
  * Administración de políticas de riesgo macro-cuantitativo.
* **Estado:** Sede Principal (Conexiones de red en standby / Despliegue futuro).

---

### Nivel 2: Nodo Operativo Edge
* **Ubicación:** Charallave, Venezuela
* **Rol:** Processing Engine / Execution Desk / Data Engine
* **Responsabilidades:**
  * Ingesta asíncrona continua (`aiohttp`, latencia ~200ms, anti-429).
  * Orquestación de 40 daemons dedicados y pipeline de scoring NLP.
  * Gestión de almacenamiento en base de datos local SQLite (WAL Mode, zero-locks).
  * Servidor local de assets PWA (:8080) y generación automática de Daily Dossiers (`crontab` 00:00 UTC/Local).
* **Estado:** Operación Continua Autónoma (Full Production).

---

## 📊 Matriz de Flujo Organizacional


