import time
import random

class M82AssetMonitor:
    def __init__(self):
        self.assets = {
            "Terminal_Nashville": {"status": "ONLINE", "efficiency": 0.98},
            "Refineria_VZ_Alpha": {"status": "OFFLINE", "efficiency": 0.0}
        }

    def scan_sensors(self, asset_name):
        print(f"\n[SENSOR] Escaneando telemetría de: {asset_name}...")
        # Simula lectura de presión, temperatura y flujo
        pressure = random.randint(80, 120)
        temp = random.randint(150, 250)
        
        if pressure > 110 or temp > 240:
            status = "WARNING"
            health_score = 0.65
        else:
            status = "OPTIMAL"
            health_score = 0.95
            
        print(f"[STATUS] {asset_name}: {status} (Health: {health_score})")
        return health_score

    def financial_impact(self, alpha_base, health_score):
        # Ajusta el retorno esperado según la salud del activo físico
        adjusted_alpha = round(alpha_base * health_score, 2)
        print(f"[FINANCE] Alpha Base: {alpha_base}% | Alpha Ajustado por Salud: {adjusted_alpha}%")
        return adjusted_alpha

if __name__ == "__main__":
    monitor = M82AssetMonitor()
    # Caso: Refinería con base de 20% de retorno
    alpha_raw = 20.0
    h_score = monitor.scan_sensors("Refineria_VZ_Alpha")
    final_return = monitor.financial_impact(alpha_raw, h_score)
