import db
from flask import request
from utils.response import error_response, good_response
from bson.objectid import ObjectId

def users_edit_user_email(id):
  '''
    Edita el parametro email del usuario
  '''    
  db_spreadsheet,db_user,db_comm = db.dbconection()
  email = request.json['email']
  if email == db_user.find_one({'_id':ObjectId(id)})['email']:
    #verify if the email is the same
    return error_response(401,'El correo no puede ser el mismo')
  if email == db_user.find_one({'email': email}): 
    #verify if the email already exists
    return error_response(401, 'El correo ya existe')
  else:
    db_user.update_one({'_id':ObjectId(id)}, {'$set': {'email': email}})
    msg = 'El correo ha sido actualizado'
    return good_response(msg)