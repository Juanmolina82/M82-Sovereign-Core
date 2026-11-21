import os, sqlite3

# 1. Purga en archivos de código (.py, .sh, .json)
targets = [f for f in os.listdir('.') if f.endswith(('.py', '.sh', '.json', '.html'))]
replacements = {
    "M82_MACRO": "M82_MACRO",
    "M82_WIRE": "M82_WIRE",
    "M82 Wire": "M82 Wire",
    "m82_macro": "m82_macro"
}

for filename in targets:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = content
        for old, new in replacements.items():
            new_content = new_content.replace(old, new)
        if new_content != content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Refactorizado: {filename}")
    except Exception as e:
        pass

# 2. Purga en la base de datos SQLite WAL
try:
    conn = sqlite3.connect('m82_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE signals SET source = 'M82_WIRE' WHERE source LIKE '%M82_WIRE%' OR source LIKE '%M82_MACRO%'")
    cursor.execute("UPDATE signals SET category = 'M82_MACRO' WHERE category LIKE '%M82_MACRO%'")
    conn.commit()
    conn.close()
    print("✅ Base de datos m82_database.db purgada de marcas registradas.")
except Exception as e:
    print(f"Error actualizando DB: {e}")

