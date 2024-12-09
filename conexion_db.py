from pymongo import MongoClient
from bson import ObjectId
import datetime

class ConexionDB:
    def __init__(self):
        # Configura la conexión a la base de datos MongoDB
        uri = "mongodb+srv://JuanSolis:Vegetta777@cluster0.3pxch.mongodb.net/PeceraBD"
        self.client = MongoClient(uri)
        self.db = self.client["PeceraBD"]

    def insertar_lectura(self, dispositivo, tipo_sensor, valor, fecha=None):
        """
        Inserta una nueva lectura en el array 'sensores' de la pecera.

        Parámetros:
        - dispositivo: El nombre del dispositivo (ej. "Pecera01").
        - tipo_sensor: El tipo de sensor (ej. "MDC").
        - valor: El valor de la lectura.
        - fecha: La fecha y hora de la lectura (se usa la fecha actual si no se proporciona).
        """
        # Si no se pasa una fecha, usar la fecha actual
        if not fecha:
            fecha = datetime.datetime.now()

        # ID del documento de la pecera donde se almacenan las lecturas
        pecera_id = ObjectId("67467ff900c28fd4180ac074")
        coleccion = self.db["Pecera"]

        # Estructura de la nueva lectura
        nueva_lectura = {
            "tipo_sensor": tipo_sensor,
            "valor": valor,
            "fecha": fecha
        }

        # Inserta la lectura en el array 'sensores' del documento correspondiente
        resultado = coleccion.update_one(
            {"_id": pecera_id},
            {"$push": {"sensores": nueva_lectura}}
        )

        # Verifica si la actualización fue exitosa
        if resultado.modified_count > 0:
            print("Lectura guardada en MongoDB correctamente.")
        else:
            print("Error al guardar la lectura en MongoDB.")
