import db
from utils.response import error_response
from bson.objectid import ObjectId
from flask import jsonify


def com_getSpreadComm(spread_id):
  '''
    Obtine todos los Comentarios de un Spreadsheet
  '''
  sort=list({
      'last_modified': -1
  }.items())
  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()
  if db_spreadsheet.find_one({'_id':ObjectId(spread_id)}):
    # verify if the spread exists
    
    comments = db_comm.find(filter={'spread_id':spread_id},sort=sort)
    response = []
    for s in comments:
      response.append({
          '_id': str(s['_id']),
          'spread_id': s['spread_id'],
          'user_id': s['user_id'],
          'username': s['username'],
          'spreadname': s['spreadname'],
          'comment': s['comment'],
          'score': s['score'],
          'last_modified': s['last_modified']
      })
    response = jsonify(response)
    response.status_code = 200
    return response
  return error_response(401, 'El spreadsheet no existe')