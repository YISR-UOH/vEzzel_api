import db
from utils.response import error_response, good_response
from bson.objectid import ObjectId

def spread_deleteSpreadsheet(id, spread_id):
  '''
    Elimina un spreadsheet
  '''
  db_spreadsheet,db_user,db_comm = db.dbconection()
  if db_user.find_one({'_id':ObjectId(id)}):
    if db_spreadsheet.find_one({'_id':ObjectId(spread_id), 'user_id':str(id)}):
      #verify if the user and spreadsheet exists
      
      
      if db_user.find_one({'_id':ObjectId(id)})['last_sheet'] == str(spread_id):
        db_user.update_one({'_id':ObjectId(id)}, {'$set': {'last_sheet': ''}})
      db_spreadsheet.delete_one({'_id':ObjectId(spread_id)})
      msg = 'El Spreadsheet ha sido eliminado'
      return good_response(msg)
    else:
      return error_response(401, 'El Spreadsheet no existe')
  
  else:
    return error_response(401, 'El usuario no existe')
