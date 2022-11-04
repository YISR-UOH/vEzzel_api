from flask import jsonify


def error_response(error,msg):
  '''
    Error 401 - Unauthorized Access 
  '''
  message = {
      'status': error,
      'message': msg
  }
  resp = jsonify(message)
  resp.status_code = 200

  return resp

def good_response(msg):
  '''
    200 - OK 
  '''
  message = {
      'status': 200,
      'message': msg
  }
  resp = jsonify(message)
  resp.status_code = 200

  return resp