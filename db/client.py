from pymongo import MongoClient
from dotenv import load_dotenv
import os


# Cargar las variables de entorno
load_dotenv()

# Obtener la URI de MongoDB desde el archivo .env
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    raise ValueError("La variable de entorno MONGO_URI no está configurada")


# Base de datos local
#db_client = MongoClient().local

# Base de datos en la nube
db_client = MongoClient(mongo_uri).test