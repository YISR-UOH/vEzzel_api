import db
from flask import request
from bson.objectid import ObjectId
from utils.response import error_response, good_response



def users_edit_user_name(id):
  '''
    Edita el parametro username del usuario
  '''
  db_spreadsheet,db_user,db_comm = db.dbconection()
  if request.json['username']:
    username = request.json['username']
    if username == db_user.find_one({'_id':  ObjectId(id)})['username']:
      #verify if the username is the same
      return error_response(401, 'El nombre de usuario no puede ser el mismo')
    if username == db_user.find_one({'username': username}):
      #verify if the username already exists
      return error_response(401, 'El nombre de usuario ya existe')
    else:
      db_user.update_one({'_id':ObjectId(id)}, {'$set': {'username': username}})
      db_spreadsheet.update_many({'user_id':id}, {'$set': {'username': username}})
      db_comm.update_many({'user_id':id}, {'$set': {'username': username}})
      msg = 'El nombre de usuario ha sido actualizado'
      
      return good_response(msg)