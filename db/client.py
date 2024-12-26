from pymongo import MongoClient
from config import settings



mongo_uri = settings.mongo_uri

if not mongo_uri:
    raise ValueError("La variable de entorno MONGO_URI no está configurada")


# Base de datos local
#db_client = MongoClient().local

# Base de datos en la nube
db_client = MongoClient(mongo_uri).test