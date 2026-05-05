import json

with open("worldbank_ve_renewable.json") as f:
    data = json.load(f)

print("Tipo raiz:", type(data))
print("Elementos raiz:", len(data))

meta, series = data[0], data[1]

print("
Claves meta:", meta.keys())
print('Ejemplo meta["total"]:', meta.get("total"))

print("
Campos disponibles en un registro de la serie:")
print(series[0].keys())

print("
Primer registro:")
print(series[0])
