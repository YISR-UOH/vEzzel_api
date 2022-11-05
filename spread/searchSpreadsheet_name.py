import db
from flask import jsonify, request
import re

def spread_searchSpreadsheet_name():
  '''
    Busca un spreadsheet por nombre y/o tags
  '''
  sort=list({
      'last_modified': -1
  }.items())
  db_spreadsheet,db_user,db_comm = db.dbconection()
  name,tags = False,False
  #tiene que devolver todo por default
  response = []
  spreadsheet = 0
  if 'name' in request.json:
    #verify if recive the name
    name = request.json['name']
  
  if 'tags' in request.json:
    #verify if recive the tags
    tags = request.json['tags']
    
  if name != False and tags == False:
    spreadsheet = db_spreadsheet.find(
      filter={'name': {
        '$regex': name, 
        '$options': 'i'
    }},
      sort=sort
    )
    
  elif name == False and tags != False:
    spreadsheet = db_spreadsheet.find(
      filter={'tags':{
        '$all':[re.compile(i,re.IGNORECASE) for i in tags]  
        }},
      sort=sort
    )

  elif name != False and tags != False:
    spreadsheet = db_spreadsheet.find(
      filter={
        'name': re.compile(name, re.IGNORECASE),
        'tags':{
        '$all':[re.compile(i,re.IGNORECASE) for i in tags]  
        }},
      sort=sort
    )
  
  elif name == False and tags == False:
    spreadsheet = db_spreadsheet.find(
      filter={},
      sort=sort
    )
  
  if spreadsheet != 0:
    for s in spreadsheet:
      response.append({
          '_id': str(s['_id']),
          'name': s['name'],
          'user_id': s['user_id'],
          'description': s['description'],
          'content': s['content'],
          'tags': s['tags'],
          'username': s['username'],
          'score': s['score'],
          "last_modified":str(s["last_modified"])
      })

  response = jsonify(response)
  response.status_code = 200
  return response
