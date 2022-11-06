import db
from flask import request, jsonify
from utils.response import error_response, good_response
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash

def users_deleteUser(id):
  '''
    Elimina al usuario y todo lo relacionado a el
  '''
  db_spreadsheet,db_user,db_comm = db.dbconection()

  if db_user.find_one({'_id': ObjectId(id)}): 
    #verify if the user already exists
    
    
    db_comm.delete_many({'user_id': id})
    db_spreadsheet.delete_many({'user_id': id})
    db_user.delete_one({'_id': ObjectId(id)})
    
    msg = 'El Usuario ha sido eliminado'
    return good_response(msg)
  else:
    return error_response(401, 'El usuario no existe')