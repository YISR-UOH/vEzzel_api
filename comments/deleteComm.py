import db
from utils.response import error_response,good_response
from bson.objectid import ObjectId


def com_deleteComm(id, spread_id,comm_id):
  '''
    Eliminar un Comentario
  '''
  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    if db_comm.find_one({'_id':ObjectId(comm_id)}):
      # verify if the comment exists
      
      score = db_comm.find_one({'_id':ObjectId(comm_id)})['score']
    
      spread = db_comm.find({'spread_id':spread_id})
      aux = 0
      n = 0
      for s in spread:
        aux+=s['score']
        n+=1
      
      spread_score = ((aux*n)- score)/n

      
      db_spreadsheet.update_one({'_id':ObjectId(spread_id)}, {'$set': {'score': spread_score}})
      db_comm.delete_one({'_id':ObjectId(comm_id)})
      msg = 'Se ha eliminado el comentario'
      return good_response(msg)
    
    return error_response(401, 'El spreadsheet no existe')
  return error_response(401, 'El usuario no existe')

