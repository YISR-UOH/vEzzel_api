import db
from flask import jsonify, request
from api.chat import Chat
from datetime import datetime
from bson.objectid import ObjectId

def chat_createChat():
  '''
    Guarda un Spreadsheet
  '''
  ['6369d0dffeeb39a914ec3a3a', '63796a23c62492e968101c6b', '13241', 'Mon Nov 21 2022 21:03:28 GMT-0300 (hora de verano de Chile)']
  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()

  user1_id = request.json['user1_id']
  user1_name = db_user.find_one({'_id':ObjectId(user1_id)})['username']
  
  user2_id = request.json['user2_id']
  user2_name = db_user.find_one({'_id':ObjectId(user2_id)})['username']
  msg = request.json['msg']
  time = request.json['time']
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
    
    chat = Chat(user1_id, user1_name, user2_id, user2_name, msg,time)
    chat_id = db_chats.insert_one(chat.toDBCollection()).inserted_id
    
    response = jsonify({'chat_id':str(chat_id),'status': 200})
    response.status_code = 200
    
    return response
    
    