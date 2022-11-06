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
      
      db_comm.update_one({'_id':ObjectId(comm_id)}, {'$set': {'comment': comment, 'score': score, 'last_modified': date_time}})
      
      spread_score = db_spreadsheet.find({'_id':ObjectId(spread_id)})['score']
      aux = 0
      n = len(spread_score)
      for i in spread_score:
        aux = aux + i.score
      
      spread_score = ((aux*n)- score_last)/n
      spread_score = ((spread_score*n)+ score)/n
      
      db_spreadsheet.update_one({'_id':ObjectId(spread_id)}, {'$set': {'score': spread_score}})
      
      response = jsonify({'id': str(comm_id),'status': 200})
      response.status_code = 200
      
      return response
    return error_response(401, 'El spreadsheet no existe')
  return error_response(401, 'El usuario no existe')


