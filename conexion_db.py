import datetime
from pymongo import MongoClient, errors
from bson import ObjectId
from archivo_json import guardar_lectura_json, leer_lecturas_json, limpiar_json

class ConexionDB:
    def __init__(self):
        self.uri = "mongodb+srv://JuanSolis:Vegetta777@cluster0.3pxch.mongodb.net/PeceraBD"
        self.db_name = "PeceraBD"
        self.collection_name = "Pecera"
        self.client = None
        self.db = None

    def conectar(self):
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.client.server_info()
            self.db = self.client[self.db_name]
            return True
        except errors.ServerSelectionTimeoutError:
            print("Conexión fallida a MongoDB.")
            return False

    def insertar_lectura(self, tipo_sensor, valor):
        fecha = datetime.datetime.now()

        if self.conectar():
            pecera_id = ObjectId("67467ff900c28fd4180ac074")
            coleccion = self.db[self.collection_name]
            lectura = {"tipo_sensor": tipo_sensor, "valor": valor, "fecha": fecha}

            try:
                resultado = coleccion.update_one(
                    {"_id": pecera_id}, {"$push": {"sensores": lectura}}
                )
                if resultado.modified_count > 0:
                    print(f"Lectura guardada en MongoDB: {lectura}")
                else:
                    print("No se pudo guardar la lectura en MongoDB.")
                    guardar_lectura_json(tipo_sensor, valor)
            except Exception as e:
                print(f"Error al guardar en MongoDB: {e}. Guardando en JSON.")
                guardar_lectura_json(tipo_sensor, valor)
        else:
            print("Sin conexión a MongoDB. Guardando lectura en JSON.")
            guardar_lectura_json(tipo_sensor, valor)

    def sincronizar_json(self):
        lecturas_pendientes = leer_lecturas_json()

        if not lecturas_pendientes:
            print("No hay lecturas pendientes para sincronizar.")
            return

        if self.conectar():
            pecera_id = ObjectId("67467ff900c28fd4180ac074")
            coleccion = self.db[self.collection_name]

            sincronizadas = True
            for lectura in lecturas_pendientes:
                try:
                    resultado = coleccion.update_one(
                        {"_id": pecera_id}, {"$push": {"sensores": lectura}}
                    )
                    if resultado.modified_count > 0:
                        print(f"Lectura sincronizada: {lectura}")
                    else:
                        sincronizadas = False
                        print(f"No se pudo sincronizar la lectura: {lectura}")
                except Exception as e:
                    sincronizadas = False
                    print(f"Error al sincronizar lectura {lectura}: {e}")

            if sincronizadas:
                limpiar_json()
            else:
                print("Algunas lecturas no pudieron sincronizarse. Archivo JSON no limpiado.")
        else:
            print("No se pudo conectar a MongoDB para sincronizar lecturas.")
