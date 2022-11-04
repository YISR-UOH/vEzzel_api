import db
from flask import jsonify, request
from utils.response import error_response
from bson.objectid import ObjectId
from api.spreadsheet import Spreadsheet
from datetime import datetime
  
def spread_editSpreadsheet(id, spread_id):
  '''
    Edita un spreadsheet
  '''

  db_spreadsheet,db_user = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    if db_spreadsheet.find_one({'_id':ObjectId(spread_id), 'user_id':str(id)}):
      #verify if the user and spreadsheet exists
      name = request.json['name']
      description = request.json['description']
      content = request.json['content']
      tags = request.json['tags']
      now = datetime.now()
      date_time = now.strftime("%Y%m%d%H%M%S%f")
      
      db_spreadsheet.update_one({'_id':ObjectId(spread_id)}, {'$set': {'name': name, 'description': description, 'content': content, 'tags': tags, "last_modified": date_time}})
      
      db_user.update_one({'_id':ObjectId(id)}, {'$set': {'last_sheet': str(spread_id)}})
      
      response = jsonify({'id': str(spread_id),'status': 200})
      response.status_code = 200
      
      return response
    else:
      #verify if the user exists
      username = db_user.find_one({'_id':ObjectId(id)})['username']
      spreadsheet = Spreadsheet(str(id),name, description, content, tags, username)
      s_id = db_spreadsheet.insert_one(spreadsheet.toDBCollection()).inserted_id
      
      db_user.update_one({'_id':ObjectId(id)}, {'$set': {'last_sheet': str(s_id)}})
      
      response = jsonify({'id': str(s_id),'status': 200})
      response.status_code = 200
      
      return response
  
  else:
    return error_response(401, 'El usuario no existe')