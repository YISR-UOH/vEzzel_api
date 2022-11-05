import db
from flask import jsonify
from utils.response import error_response
from bson.objectid import ObjectId

def spread_getLastSpreadsheet(id):
  '''
    Obtiene el último spreadsheet modificado
  '''
  db_spreadsheet,db_user,db_comm = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    last_modified = db_user.find_one({'_id':ObjectId(id)})['last_sheet']
    if last_modified != '':
      spreadsheet = db_spreadsheet.find_one({'_id':ObjectId(last_modified)})
      response = {
          '_id': str(spreadsheet['_id']),
          'name': spreadsheet['name'],
          'user_id': spreadsheet['user_id'],
          'description': spreadsheet['description'],
          'content': spreadsheet['content'],
          'tags': spreadsheet['tags'],
          'score': spreadsheet['score'],
          'username': spreadsheet['username'],
          'last_modified': spreadsheet['last_modified']
      }
      response = jsonify(response)
      response.status_code = 200
      return response
    else:
      return error_response(401, 'El usuario no tiene un Spreadsheet modificado')
  return error_response(401, 'El usuario no existe')
 