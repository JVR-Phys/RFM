from pathlib import Path
from datetime import datetime
import json

r = Path(__file__).resolve().parent
json_path = r / "../src/actividades.json"

# 1. Cargar datos existentes si el archivo ya existe
if json_path.exists():
    with open(json_path, 'r', encoding='utf-8') as f:
        datos_json = json.load(f)
        lista_actividades = datos_json.get("actividades", [])
else:
    lista_actividades = []

# Creamos un set de URLs existentes para saber qué archivos ya procesamos
urls_procesadas = {act["url"] for act in lista_actividades}

# Determinar el último ID utilizado
ultimo_id = lista_actividades[-1]["id"] if lista_actividades else 0

padres = ["1", "2", "3", "4", "5", "6"]
nuevos_archivos_raw = []

# 2. Buscar archivos en las carpetas
for padre in padres:
    ruta_act = r / ".." / padre / "src" / "actividades"
    
    if ruta_act.exists() and ruta_act.is_dir():
        for archivo in ruta_act.iterdir():
            if archivo.is_file():
                # Construimos la URL de este archivo para comparar
                # Usamos la misma lógica de construcción que antes
                nombre_padre = archivo.parts[-4] if len(archivo.parts) >= 4 else "parentX"
                ruta_url = f"./{nombre_padre}/src/actividades/{archivo.name}"

                # SOLO lo agregamos si NO está en el JSON
                if ruta_url not in urls_procesadas:
                    stats = archivo.stat()
                    nuevos_archivos_raw.append({
                        "archivo": archivo,
                        "fecha_raw": stats.st_mtime,
                        "url": ruta_url,
                        "nombre_padre": nombre_padre
                    })

# 3. Ordenar solo los NUEVOS por fecha
nuevos_archivos_raw.sort(key=lambda x: x["fecha_raw"])

# 4. Procesar y agregar los nuevos a la lista principal
for item in nuevos_archivos_raw:
    ultimo_id += 1
    archivo_path = item["archivo"]
    nombre_sin_ext = archivo_path.stem
    
    # Construcción de la nueva entrada
    nueva_actividad = {
        "id": ultimo_id,
        "titulo": "", 
        "imagen": f"./{item['nombre_padre']}/src/img/{nombre_sin_ext}.jpg",
        "url": item["url"]
    }
    lista_actividades.append(nueva_actividad)

# 5. Guardar el resultado final (Sobreescribe el archivo con la lista aumentada)
json_final = {"actividades": lista_actividades}

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_final, f, indent=2, ensure_ascii=False)

print(f"Proceso terminado. Se agregaron {len(nuevos_archivos_raw)} archivos nuevos.")