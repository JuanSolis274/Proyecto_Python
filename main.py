import time
from conexion_db import ConexionDB


def procesar_datos(datos):
    db = ConexionDB()
    db.sincronizar_json()  # Sincronizar lecturas pendientes antes de procesar nuevas

    try:
        tipo_sensor, valor = datos.split(":")
        valor = float(valor)
        db.insertar_lectura(tipo_sensor, valor)
    except Exception as e:
        print(f"Error al procesar datos: {e}")


def leer_datos_desde_arduino():
    # Simular datos recibidos desde Arduino (reemplazar con datos reales)
    sensores = ["PH", "MDC", "NDA", "TURB", "TEMP"]
    import random
    while True:
        for sensor in sensores:
            valor = round(random.uniform(0.1, 100), 2)
            yield f"{sensor}:{valor}"


if __name__ == "__main__":
    datos_arduino = leer_datos_desde_arduino()
    for datos in datos_arduino:
        print(f"Datos recibidos: {datos}")
        procesar_datos(datos)
        time.sleep(2)  # Simular intervalo de tiempo entre lecturas
