from PIL import Image, ImageDraw
img = Image.new('RGB', (1080, 1080), color=(10, 10, 10))
d = ImageDraw.Draw(img)
text = "M82 ARCHITECTURE\nSOVEREIGN CUSTODY SYSTEM\n\nVERDICT: SOLVENCY CONFIRMED\nENERGY ANCHOR: 07.97\n\nNON-NEGOTIABLE"
d.text((100, 400), text, fill=(0, 255, 0))
img.save('M82_SOVEREIGN.png')
print("--- IMAGEN DE AUTORIDAD GENERADA: M82_SOVEREIGN.png ---")
