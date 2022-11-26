import db
from flask import jsonify, request
from api.chat import Chat
from datetime import datetime
from bson.objectid import ObjectId

def chat_saveChat(data):
  '''
    Guarda un Spreadsheet
  '''
  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()
  user1_id = data[0]
  user1_name = db_user.find_one({'_id':ObjectId(user1_id)})['username']
  
  user2_id = data[1]
  user2_name = db_user.find_one({'_id':ObjectId(user2_id)})['username']
  msg = data[2]
  time = data[3]
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
    db_chats.update_one(filter, {'$push': {'msg': [user1_id,user2_id,msg,time]},'$set': {'time': time}})
    
    response = jsonify({'status': 200})
    response.status_code = 200
    
    return response
  else:
    #create chat
    
    chat = Chat(user1_id, user1_name, user2_id, user2_name, msg)
    chat_id = db_chats.insert_one(chat.toDBCollection()).inserted_id
    
    response = jsonify({'chat_id':str(chat_id),'status': 200})
    response.status_code = 200
    
    return response
    
    
    
    
    
