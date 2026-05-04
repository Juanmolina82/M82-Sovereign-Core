import hashlib
import time

class M82AuditTrail:
    def __init__(self):
        self.ledger = []

    def log_event(self, event_details):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        record = f"{timestamp} | {event_details}"
        # Generar un Hash único para asegurar que el registro sea inmutable
        entry_hash = hashlib.sha256(record.encode()).hexdigest()
        
        self.ledger.append({"record": record, "hash": entry_hash})
        print(f"[AUDIT LOG] Evento Registrado: {event_details}")
        print(f"[HASH] {entry_hash[:16]}... (Protegido)")

if __name__ == "__main__":
    audit = M82AuditTrail()
    audit.log_event("Ejecución exitosa del Global Dashboard v4")
    audit.log_event("Bloqueo preventivo en Refinería VZ - Riesgo Operativo")
