import json

# Leer el archivo JSON original
with open('regionescomuna.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Lista para almacenar las nuevas entradas
new_data = []

# Iterar sobre cada región y sus comunas
for entry in data:
    region = entry['fields']['region']
    comunas = entry['fields']['comunas']
    
    # Crear una nueva entrada para cada comuna
    for comuna in comunas:
        new_entry = {
            "model": "web.comuna",
            "fields": {
                "nombre": comuna,
                "region": region
            }
        }
        new_data.append(new_entry)

# Escribir el nuevo archivo JSON
with open('comunas.json', 'w', encoding='utf-8') as file:
    json.dump(new_data, file, ensure_ascii=False, indent=2)