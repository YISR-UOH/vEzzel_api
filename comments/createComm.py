import db
from flask import jsonify, request
from utils.response import error_response
from bson.objectid import ObjectId
from api.comments import Comments


def com_createComm(id, spread_id):
  '''
    Guarda un comentario
  '''
  db_spreadsheet,db_user,db_comm = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    if db_spreadsheet.find_one({'_id':ObjectId(spread_id)}):
      # verify if the spreadsheet exists
      comment = request.json['comment']
      score = request.json['score']
      
      username = db_user.find_one({'_id':ObjectId(id)})['username']
      spreadname = db_spreadsheet.find_one({'_id':ObjectId(spread_id)})['name']

      comments = Comments(str(spread_id),str(id), comment, score, username, spreadname)
      c_id = db_comm.insert_one(comments.toDBCollection()).inserted_id
      
      spread_score = db_spreadsheet.find_one({'_id':ObjectId(spread_id)})['score']
      if spread_score == 0:
        spread_score = score
      else:
        spread_score = (spread_score + score)/2
      
      db_spreadsheet.update_one({'_id':ObjectId(spread_id)}, {'$set': {'score': spread_score}})
      
      response = jsonify({'id': str(c_id),'status': 200})
      response.status_code = 200
      
      return response
    return error_response(401, 'El spreadsheet no existe')
  return error_response(401, 'El usuario no existe')