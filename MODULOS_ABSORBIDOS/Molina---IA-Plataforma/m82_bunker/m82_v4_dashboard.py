import time

class M82GlobalDashboard:
    def __init__(self, firm_name):
        self.firm = firm_name
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    def generate_executive_summary(self, assets_data):
        print(f"\n{'='*60}")
        print(f"       {self.firm} - GLOBAL COMMAND DASHBOARD")
        print(f"       Timestamp: {self.timestamp}")
        print(f"{'='*60}")
        
        total_aum_exposure = 0
        
        for asset in assets_data:
            print(f"\n[ASSET: {asset['name']}]")
            print(f" > Jurisdicción: {asset['loc']}")
            print(f" > Status Operativo: {asset['status']}")
            print(f" > Alpha Proyectado: {asset['alpha']}%")
            
            if asset['alpha'] < 15:
                print(" > NOTA: Rendimiento bajo observación técnica.")
            
            total_aum_exposure += 1
            
        print(f"\n{'='*60}")
        print(f" TOTAL ACTIVOS BAJO MONITOREO M82: {total_aum_exposure}")
        print(f" ESTADO DE DERECHO VZ: ESPERANDO MARCO JURÍDICO")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    # Datos consolidados de las ejecuciones anteriores
    data_points = [
        {"name": "Molina_Feeder_Delaware", "loc": "USA", "status": "OPTIMAL", "alpha": 19.76},
        {"name": "Refineria_VZ_Alpha", "loc": "VENEZUELA", "status": "WARNING", "alpha": 13.0}
    ]
    
    board_view = M82GlobalDashboard("MOLINA HOLDINGS LLC")
    board_view.generate_executive_summary(data_points)
