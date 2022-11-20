from pymongo import MongoClient
import os


def dbconection():
  #mongodb+srv://vEzzel:v3zzel_Web_Company@vezzel.lgiwpov.mongodb.net/?retryWrites=true&w=majority

  #os.getenv("MONGODB_URI")
  MONGO_URI = os.getenv("MONGODB_URI")

  client = MongoClient(MONGO_URI)
  db = client.vEzzel
  db_spreadsheet = db['spreads']
  db_user = db['users']
  db_comm = db['comments']
  db_chats = db['chats']
  return db_spreadsheet, db_user, db_comm, db_chats
    