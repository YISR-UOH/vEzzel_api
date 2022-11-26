import db
from flask import jsonify, request
from bson.objectid import ObjectId
def chat_getAllChat():
  '''
    Retorna todos los chat del usuario
  '''
  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()

  user1_id = request.json['user1_id']
  user1_name = db_user.find_one({'_id':ObjectId(user1_id)})['username']
  
  filter={
    'users': {
        '$all': [
            [
                user1_id, user1_name
            ]
        ]
    }
  }
  sort=list({
    'time': 1
  }.items())
  
  if db_chats.find_one(filter=filter):
    #verify if the chat exists
      chats = db_chats.find(filter=filter,sort=sort)
      response = []
      for s in chats:
        response.append({
            '_id': str(s['_id']),
            'users': s['users'],
            'msg': s['msg'],
            'time': s['time']
        })
      response = jsonify(response)
      response.status_code = 200
      return response
    
  else:
    response = []

    
    response = jsonify(response)
    response.status_code = 200
    
    return response