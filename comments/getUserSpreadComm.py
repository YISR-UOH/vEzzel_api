import db
from utils.response import error_response
from bson.objectid import ObjectId
from flask import jsonify


def com_getUserSpreadComm(id,spread_id):
  '''
    Obtiene el comentario del usuario de un spreadsheet
  '''
  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    if db_spreadsheet.find_one({'_id':ObjectId(spread_id)}):
      # verify if the spread exists
      if db_comm.find_one({'spread_id':spread_id,'user_id':id}):
        comments = db_comm.find_one({'spread_id':spread_id,'user_id':id})  
        response = {
            '_id': str(comments['_id']),
            'spread_id': comments['spread_id'],
            'user_id': comments['user_id'],
            'username': comments['username'],
            'spreadname': comments['spreadname'],
            'comment': comments['comment'],
            'score': comments['score'],
            'last_modified': comments['last_modified']
        }
        response = jsonify(response)
        response.status_code = 200
        return response
      return error_response(401, 'El spreadsheet no tiene comentarios del usuario')
    
    return error_response(401, 'El spreadsheet no existe')
  return error_response(401, 'El usuario no existe')
