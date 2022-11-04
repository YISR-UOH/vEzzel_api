import db
from flask import jsonify
from utils.response import error_response
from bson.objectid import ObjectId

def spread_getSpreadsheet(id):
  '''
    Retorna las Spreadsheet del usuario
  '''
  sort=list({
      'last_modified': -1
  }.items())

  db_spreadsheet,db_user = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    spreadsheet = db_spreadsheet.find(filter={'user_id':id},sort=sort)
    response = []
    for s in spreadsheet:
      response.append({
          '_id': str(s['_id']),
          'name': s['name'],
          'user_id': s['user_id'],
          'description': s['description'],
          'content': s['content'],
          'tags': s['tags'],
          'username': s['username'],
          'last_modified': s['last_modified']
      })
    response = jsonify(response)
    response.status_code = 200
    return response
  return error_response(401, 'El usuario no tiene Spreadsheet')