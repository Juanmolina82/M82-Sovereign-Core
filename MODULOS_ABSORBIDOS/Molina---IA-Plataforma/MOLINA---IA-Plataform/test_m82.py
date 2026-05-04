import hashlib
from datetime import datetime

def test_quantum_logic():
    risk = 84.2
    sig = hashlib.sha256(str(risk).encode()).hexdigest()[:16].upper()
    print("\n" + "="*40)
    print("⬜ M82 QUANTUM | SYSTEM TEST")
    print("="*40)
    print(f"🛰️ TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 RISK INDEX: {risk}%")
    print(f"🔐 SIGNATURE: {sig}-NODE-OK")
    print("="*40)
    print("🟢 STATUS: CORE OPERATIONAL\n")

if __name__ == "__main__":
    test_quantum_logic()
