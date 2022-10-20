from pymongo import MongoClient


MONGO_URI = 'mongodb+srv://vEzzel:v3zzel_Web_Company@vezzel.lgiwpov.mongodb.net/?retryWrites=true&w=majority'


def dbConnection():
    try:
        client = MongoClient(MONGO_URI)
        db = client.vEzzel
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db