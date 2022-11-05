import db
from flask import jsonify, request
from utils.response import error_response
from bson.objectid import ObjectId


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
      db_comm.update_one({'_id':ObjectId(comm_id)}, {'$set': {'comment': comment, 'score': score}})
      spread_score = db_spreadsheet.find_one({'_id':ObjectId(spread_id)})['score']
      if spread_score == 0:
        spread_score = score
      else:
        spread_score = (spread_score + score)/2
      
      db_spreadsheet.update_one({'_id':ObjectId(spread_id)}, {'$set': {'score': spread_score}})
      
      response = jsonify({'id': str(comm_id),'status': 200})
      response.status_code = 200
      
      return response
    return error_response(401, 'El spreadsheet no existe')
  return error_response(401, 'El usuario no existe')