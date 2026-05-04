import time

def rba_monitor():
    print("--- M82 SOVEREIGN ENGINE ACTIVATED ---")
    while True:
        print(f"\n[ALERTA RBA] {time.strftime('%H:%M:%S')}")
        print("ESTADO: BRENT $110.45 | DXY 98.89")
        print("DECISIÓN: Ejecutar Tolling Agreement en Serie 2028.")
        time.sleep(10)

if __name__ == '__main__':
    rba_monitor()
