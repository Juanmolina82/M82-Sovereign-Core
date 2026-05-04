import datetime

class MolinaStrategicInfrastructure:
    def __init__(self):
        self.firm = "Molina Holdings LLC"
        self.brent_spot = 110.72 #
        self.futures_pullback = -3.47 #
        
    def report(self):
        print(f"🏛️ {self.firm} - STATUS ACTIVE")
        print(f"BRENT: ${self.brent_spot} | FUTUROS: {self.futures_pullback}%")

if __name__ == "__main__":
    m82 = MolinaStrategicInfrastructure()
    m82.report()
