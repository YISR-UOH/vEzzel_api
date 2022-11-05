import db
from flask import request
from bson.objectid import ObjectId
from utils.response import error_response, good_response
from utils.passcheck import password_check
from werkzeug.security import generate_password_hash, check_password_hash



def users_edit_user_pass(id):
  '''
    Edita el parametro password del usuario
  '''    
  db_spreadsheet,db_user,db_comm = db.dbconection()
  password = request.json['password']
  if check_password_hash(db_user.find_one({'_id':ObjectId(id)})['password'],password):
    #verify if the password is the same
    return error_response(401,'La contraseña no puede ser la misma')
  pass_strong = password_check(password)
  if pass_strong==True:
    #verify if the password is strong
    hashed_password = generate_password_hash(password)
    db_user.update_one({'_id':ObjectId(id)}, {'$set': {'password': hashed_password}})
    msg = 'La contraseña ha sido actualizada'
    return good_response(msg)
  else:
    return error_response(401, pass_strong) 