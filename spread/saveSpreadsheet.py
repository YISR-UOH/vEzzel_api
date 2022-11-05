import db
from flask import jsonify, request
from utils.response import error_response
from bson.objectid import ObjectId
from api.spreadsheet import Spreadsheet


def spread_saveSpreadsheet(id):
  '''
    Guarda un Spreadsheet
  '''
  db_spreadsheet,db_user,db_comm = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    name = request.json['name']
    description = request.json['description']
    content = request.json['content']
    tags = request.json['tags']
    username = db_user.find_one({'_id':ObjectId(id)})['username']
    
    spreadsheet = Spreadsheet(str(id),name, description, content, tags, username)
    s_id = db_spreadsheet.insert_one(spreadsheet.toDBCollection()).inserted_id
    
    db_user.update_one({'_id':ObjectId(id)}, {'$set': {'last_sheet': str(s_id)}})
    
    response = jsonify({'id': str(s_id),'status': 200})
    response.status_code = 200
    
    return response
  return error_response(401, 'El usuario no existe')