import db
from flask import jsonify
from utils.response import error_response
from bson.objectid import ObjectId

def spread_getOneSpread(spread_id):
  '''
    Retorna la Spreadsheet 
  '''

  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()
  if db_spreadsheet.find_one({'_id':ObjectId(spread_id)}):
    #verify if the spread exists
    spreadsheet = db_spreadsheet.find_one({'_id':ObjectId(spread_id)})
    response={
          '_id': str(spreadsheet['_id']),
          'name': spreadsheet['name'],
          'user_id': spreadsheet['user_id'],
          'description': spreadsheet['description'],
          'content': spreadsheet['content'],
          'tags': spreadsheet['tags'],
          'username': spreadsheet['username'],
          "score": spreadsheet['score'],
          'last_modified': spreadsheet['last_modified']
    }
    response = jsonify(response)
    response.status_code = 200
    return response
  return error_response(401, 'La spreadsheet no existe')