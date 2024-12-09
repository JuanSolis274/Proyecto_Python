import serial
import time
from conexion_db import ConexionDB

def leer_datos_serial(puerto):
    # Configura el puerto serial
    try:
        ser = serial.Serial(puerto, 9600, timeout=1)  # Ajusta el puerto y la velocidad según sea necesario
        time.sleep(2)  # Espera a que se establezca la conexión
        while True:
            if ser.in_waiting > 0:
                # Lee la línea de datos enviada por Arduino
                data = ser.readline().decode('utf-8').strip()
                if data:
                    return data
    except Exception as e:
        print(f"Error al leer desde el puerto serial: {e}")
        return None

def procesar_datos(datos):
    """
    Procesa los datos recibidos desde Arduino. Se espera que los datos
    sean en formato 'tipo_sensor:valor' (ej. 'MDC:45.8').
    """
    try:
        tipo_sensor, valor = datos.split(":")
        return tipo_sensor, float(valor)
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return None, None

def main():
    db = ConexionDB()  # Instancia la clase para interactuar con la DB
    puerto = "COM5"  # Especifica el puerto serial (ajústalo según tu sistema)
    
    while True:
        # Leer datos del puerto serial (sensor de Arduino)
        datos = leer_datos_serial(puerto)
        
        if datos:
            tipo_sensor, valor = procesar_datos(datos)
            
            if tipo_sensor and valor is not None:
                # Enviar los datos a MongoDB
                fecha = time.strftime('%Y-%m-%d %H:%M:%S')  # Fecha en formato adecuado
                db.insertar_lectura("Pecera01", tipo_sensor, valor, fecha)
        
        # Esperar un intervalo antes de leer los siguientes datos
        time.sleep(5)  # Ajusta el intervalo según sea necesario

if __name__ == "__main__":
    main()
