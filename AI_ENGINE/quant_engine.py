import time, json, os

def get_kelly(cap, price, win, rr):
    f = (win * (rr + 1) - 1) / rr
    safe_f = f * 0.5 
    alloc = cap * safe_f
    return safe_f * 100, alloc, alloc / price

cap = 1000000
assets = {
    "NVDA": [142.45, 0.72, 2.5],
    "BTC":  [70343.0, 0.55, 3.0],
    "GOLD": [2345.1, 0.60, 1.5]
}

print("M82: Motor Cuantitativo Online")

while True:
    res = {}
    print(f"\n--- SYNC: {time.strftime('%H:%M:%S')} ---")
    for t, d in assets.items():
        p, c, q = get_kelly(cap, d[0], d[1], d[2])
        res[t] = {"k": f"{p:.2f}%", "usd": f"${c:,.0f}", "u": f"{q:.4f}"}
        print(f"[{t}] Kelly: {p:.2f}%")
    
    with open('m82_recommendations.json', 'w') as f:
        json.dump(res, f)
    
    time.sleep(60)
o

