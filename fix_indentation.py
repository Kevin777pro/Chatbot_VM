# Leer el archivo
with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Corregir la indentación de la línea 740 (índice 739)
if lines[739].startswith("        # Input del usuario con opción de voz"):
    lines[739] = "    # Input del usuario con opción de voz\n"

# Escribir el archivo
with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Indentación corregida exitosamente")
