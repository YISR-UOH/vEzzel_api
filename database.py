from pymongo import MongoClient
import certifi
import os

MONGO_URI = os.getenv("MONGODB_URI")
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client.vEzzel
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db