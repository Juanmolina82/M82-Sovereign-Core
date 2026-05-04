from PIL import Image, ImageDraw, ImageFont

# Crear lienzo 16:9 para LinkedIn (profesional)
img = Image.new('RGB', (1200, 627), color=(5, 5, 15))
d = ImageDraw.Draw(img)

# Simular una interfaz de Trading de Alta Frecuencia
d.rectangle([0, 0, 1200, 50], fill=(20, 20, 40)) # Barra superior
d.text((20, 15), "MOLINA HOLDINGS LLC | M82 ARCHITECTURE | TERMINAL v2.2", fill=(200, 200, 200))

# Cuerpo del mensaje con estética de Hedge Fund
header = "SOVEREIGN CUSTODY SYSTEM"
sub_header = "ASSET CLASS: MACRO ENERGY & REAL ASSETS"
status = "STATUS: OPERATIONAL - SOLVENCY CONFIRMED"
energy = "ENERGY ANCHOR: $107.97 / BBL"
legal = "PDI CLAIMS: SECURED - NON-NEGOTIABLE"

d.text((100, 150), header, fill=(0, 255, 150)) # Verde Neón / Bloomberg
d.text((100, 220), sub_header, fill=(255, 255, 255))
d.text((100, 300), status, fill=(255, 165, 0)) # Naranja de Alerta/Acción
d.text((100, 380), energy, fill=(255, 255, 255))
d.text((100, 460), legal, fill=(255, 255, 255))

# Sello de Agua del Hedge Fund
d.text((900, 550), "M82 STRATEGY", fill=(50, 50, 80))

img.save('M82_LINKEDIN_PREMIUM.png')
print("--- IMAGEN DE ALTO IMPACTO GENERADA PARA LINKEDIN ---")
