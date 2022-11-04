import db
from flask import jsonify
from bson.objectid import ObjectId
def users_getAll():
  '''
    Lista todos los usuarios
  '''
  db_spreadsheet,db_user = db.dbconection()
  users = []
  for doc in db_user.find():
      users.append({
          '_id': str(ObjectId(doc['_id'])),
          'username': doc['username'],
          'email': doc['email'],
          'password': doc['password']
      })
  return jsonify(users)