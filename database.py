from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os


load_dotenv()

MONGO_URI = f'mongodb+srv://vEzzel:{os.environ.get("password")}'\
    '@vezzel.lgiwpov.mongodb.net/?retryWrites=true&w=majority'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client.vEzzel
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db