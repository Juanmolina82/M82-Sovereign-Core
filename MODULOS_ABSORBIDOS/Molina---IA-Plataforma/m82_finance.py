def calcular_arbitraje(precio_actual, posicion_inicial=105.00, barriles=1000):
    diferencia = precio_actual - posicion_inicial
    ganancia_neta = diferencia * barriles
    return ganancia_neta

if __name__ == "__main__":
    brent = 110.72
    resultado = calcular_arbitraje(brent)
    print(f"--- ANALÍTICA MOLINA HOLDINGS ---")
    print(f"Brent Actual: ${brent}")
    print(f"Ganancia Proyectada: ${resultado} USD")
