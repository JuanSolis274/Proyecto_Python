import json
from datetime import datetime

ARCHIVO_JSON = "lecturas_pendientes.json"

def guardar_lectura_json(tipo_sensor, valor):
    lectura = {
        "tipo_sensor": tipo_sensor,
        "valor": valor,
        "fecha": datetime.now().isoformat()
    }

    try:
        try:
            with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
                lecturas = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            lecturas = []

        lecturas.append(lectura)

        with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
            json.dump(lecturas, archivo, indent=4)

        print(f"Lectura guardada en JSON: {lectura}")
    except Exception as e:
        print(f"Error al guardar la lectura en JSON: {e}")

def leer_lecturas_json():
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def limpiar_json():
    try:
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
            json.dump([], archivo, indent=4)
        print("Archivo JSON limpiado.")
    except Exception as e:
        print(f"Error al limpiar el archivo JSON: {e}")
