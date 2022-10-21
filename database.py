from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://vEzzel:v3zzel_Web_Company@vezzel.lgiwpov.mongodb.net/?retryWrites=true&w=majority'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client.vEzzel
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db