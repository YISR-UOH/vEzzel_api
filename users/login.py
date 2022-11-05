import db
from flask import request, jsonify
from utils.response import error_response, good_response
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash

def users_login():
  '''
    Verifica que el usuario exista y que la contraseña sea correcta
  '''
  db_spreadsheet,db_user,db_comm = db.dbconection()
  email = request.json['email']
  password = request.json['password']
  if db_user.find_one({'email':email}) and check_password_hash(db_user.find_one({'email':email})['password'],password):
    #verify if the email and password are correct
    id = db_user.find_one({'email':email})['_id']
    response = jsonify({'id': str(id),'status': 200})
    response.status_code = 200
    return response
  
  else:
    return error_response(401, 'Usuario o contraseña incorrectos')