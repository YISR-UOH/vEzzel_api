import db
from flask import jsonify, request
from utils.response import error_response
from bson.objectid import ObjectId
from datetime import datetime

def com_editComm(id, spread_id,comm_id):
  '''
    Edita un Comentario
  '''
  db_spreadsheet,db_user,db_comm = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    if db_comm.find_one({'_id':ObjectId(comm_id)}):
      # verify if the comment exists
      comment = request.json['comment']
      score = request.json['score']
      now = datetime.now()
      date_time = now.strftime("%Y%m%d%H%M%S%f")
      
      score_last = db_comm.find_one({'_id':ObjectId(comm_id)})['score']
      
      if db_comm.find({'spread_id':spread_id}):
        spread = db_comm.find({'spread_id':spread_id})
        aux = 0
        n = 0
        for s in spread:
          aux+=s['score']
          n+=1
        spread_score = ((aux)- score_last)/(n)
        if n==1:
          spread_score = ((spread_score)+ score)
        else:
          spread_score = ((spread_score*n)+ score)/(n)
      else:
        spread_score = score
        
      db_comm.update_one({'_id':ObjectId(comm_id)}, {'$set': {'comment': comment, 'score': score, 'last_modified': date_time}})
      db_spreadsheet.update_one({'_id':ObjectId(spread_id)}, {'$set': {'score': spread_score}})
      
      response = jsonify({'id': str(comm_id),'status': 200})
      response.status_code = 200
      
      return response
    return error_response(401, 'El spreadsheet no existe')
  return error_response(401, 'El usuario no existe')


