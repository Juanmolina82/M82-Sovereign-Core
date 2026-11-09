import time, logging

logging.basicConfig(filename='m82_ib.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def calc_position_sizing(risk_score, vol_curve="Brent"):
    if risk_score >= 9.0:
        return 3
    elif risk_score >= 8.5:
        return 2
    return 1

if __name__ == "__main__":
    logging.info("🚀 [M82 IB GATEWAY] Modo Híbrido Activo (Paper :7497 / Live :7496)")
    print("🚀 [M82 IB GATEWAY] Daemon activo en background. Revisa logs en m82_ib.log")
    while True:
        time.sleep(60)
