import db
from flask import jsonify, request
from api.chat import Chat
from datetime import datetime

def chat_saveChat():
  '''
    Guarda un Spreadsheet
  '''
  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()
  
  user1_id = request.json['user1_id']
  user1_name = request.json['user1_name']
  user2_id = request.json['user2_id']
  user2_name = request.json['user2_name']
  msg = request.json['msg']
  now = datetime.now()
  time = now.strftime("%Y%m%d%H%M%S%f")
  filter={
    'users': {
        '$all': [
            [
                user1_id, user1_name
            ], [
                user2_id, user2_name
            ]
        ]
    }
  }
  if db_chats.find_one(filter=filter):
    #verify if the chat exists
    db_chats.update_one(filter, {'$push': {'msg': [user1_id,msg,time]},'$set': {'time': time}})
    
    response = jsonify({'status': 200})
    response.status_code = 200
    
    return response
  else:
    #create chat
    
    chat = Chat(user1_id, user1_name, user2_id, user2_name, msg)
    chat_id = db_chats.insert_one(chat.toDBCollection()).inserted_id
    
    response = jsonify({'status': 200})
    response.status_code = 200
    
    return response
    
    
    
    
    
