import time
import serial
from conexion_db import ConexionDB


def procesar_datos(datos):
    db = ConexionDB()
    db.sincronizar_json()

    try:
        tipo_sensor, valor = datos.split(":")
        valor = float(valor)
        db.insertar_lectura(tipo_sensor, valor)
    except Exception as e:
        print(f"Error al procesar datos: {e}")


def leer_datos_desde_arduino(puerto_serie):
    """
    Lee datos enviados por el Arduino a través del puerto serie.
    """
    try:
        puerto = serial.Serial(puerto_serie, baudrate=9600, timeout=1)
        print(f"Conexión establecida con Arduino en {puerto_serie}.")

        while True:
            linea = puerto.readline().decode("utf-8").strip()
            if linea:
                yield linea

    except serial.SerialException as e:
        print(f"Error de conexión con Arduino: {e}")
        exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        exit(1)


if __name__ == "__main__":
    # Cambia el puerto según el dispositivo conectado
    puerto_serie = "/dev/ttyUSB0"  # Verifica si es el puerto correcto

    datos_arduino = leer_datos_desde_arduino(puerto_serie)

    for datos in datos_arduino:
        print(f"Datos recibidos: {datos}")
        procesar_datos(datos)
        time.sleep(2)
