def draw_chart(ticker, value, max_val=100):
    bar_length = int((value / max_val) * 20)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    print(f"{ticker:10} | {bar} | {value}% Strength")

print("\n--- MOLINA HOLDINGS: ASSET STRENGTH VISUALIZER ---")
data = {"SNDK": 88, "CRDO": 92, "AAL": 65, "NVDA_CORR": 45}

for ticker, strength in data.items():
    draw_chart(ticker, strength)
print("--------------------------------------------------")
