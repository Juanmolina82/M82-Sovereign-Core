import time
import random
import math
from datetime import datetime

class M82_LSTM_Engine:
    def __init__(self):
        # Estado inicial de la celda de memoria (Long-term memory)
        self.cell_state = 0.5 
        self.hidden_state = 0.1
        print(f"\033[95m[SISTEMA] Arquitectura LSTM Inicializada correctamente.\033[0m")

    def forward_pass(self, x_t):
        # Simulación matemática de las Gates (Puertas) de tu imagen
        forget_gate = 1 / (1 + math.exp(-random.uniform(0.5, 1.5))) # Decide qué olvidar del SOX
        input_gate = 1 / (1 + math.exp(-random.uniform(-1, 1)))    # Decide qué aprender de Intel hoy
        output_gate = 1 / (1 + math.exp(-random.uniform(0, 1)))     # Decide qué predecir
        
        # Actualización de la Celda (Memory Cell)
        self.cell_state = (self.cell_state * forget_gate) + (input_gate * math.tanh(x_t))
        self.hidden_state = math.tanh(self.cell_state) * output_gate
        
        return self.hidden_state

def run_prediction_loop():
    brain = M82_LSTM_Engine()
    current_price = 79.82  # Precio real de Intel en tu captura
    
    print("\n" + "="*65)
    print("M82 NEURAL PREDICTOR v5.0 - DEEP LEARNING LAYER")
    print("MODEL: LSTM (Long Short-Term Memory) | TARGET: INTC/SOX")
    print("="*65 + "\n")
    
    try:
        while True:
            # Normalizamos el precio para la red
            normalized_input = (current_price / 100) - 0.5
            prediction_factor = brain.forward_pass(normalized_input)
            
            # Generamos la proyección
            projected_price = current_price * (1 + (prediction_factor * 0.02))
            trend = "ACCUMULATION" if prediction_factor > 0 else "DISTRIBUTION"
            color = "\033[92m" if prediction_factor > 0 else "\033[91m"
            
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] INPUT: ${current_price:.2f} | NEURAL PROJECTION: {color}${projected_price:.2f} ({trend})\033[0m")
            
            # Simulamos el tick del mercado
            current_price += random.uniform(-0.10, 0.12)
            time.sleep(2.5)
            
    except KeyboardInterrupt:
        print("\n[INFO] Motor Neuronal pausado. Memoria de celda preservada.")

if __name__ == "__main__":
    run_prediction_loop()
