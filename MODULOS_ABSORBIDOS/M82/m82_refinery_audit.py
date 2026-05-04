# -*- coding: utf-8 -*-
# M82 REFINERY & CRACK SPREAD MONITOR - 27 APR 2026
# Source: Reuters (Ahmad Ghaddar) | Europe Gasoline

class RefineryAudit:
    def __init__(self):
        self.ebob_crack = "$20.25/bbl (Down from $22.26)"
        self.incident = "BP Whiting Power Outage (Indiana)"
        self.eu_exports = "886,000 bpd (Declining trend)"
        self.market_signal = "Upstream Value > Downstream Risk"

    def log_to_core(self):
        print("\n" + "⛽ "*15)
        print("     M82 SOVEREIGN AUDIT: REFINING PRESSURE")
        print("⛽ "*15)
        print(f"MÁRGENES NWE: {self.ebob_crack}")
        print(f"ALERTA INFRA: Fallo de energía en Whiting detectado.")
        print(f"ESTRATEGIA: El valor se refugia en el crudo físico del Nodo Caribe.")
        print("-" * 60)
        print("REGISTRO: Confirmación de estrés en infraestructura de refinación.")
        print("⛽ "*15 + "\n")

if __name__ == "__main__":
    RefineryAudit().log_to_core()
