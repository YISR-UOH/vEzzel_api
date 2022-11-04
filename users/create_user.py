import db
from flask import jsonify,request
from api.user import User
from utils.passcheck import password_check
from werkzeug.security import generate_password_hash
from utils.response import error_response

def users_create_user():
  '''
    Crea un usuario en la base de datos, si no existe ya un usuario con el mismo nombre de usuario o email;
    verifica que la contraseña tenga al menos 8 caracteres, un dígito, una letra mayúscula y una letra minúscula
  '''
  db_spreadsheet,db_user = db.dbconection()
  val = True
  msg = {}
  username = request.json['username']
  email = request.json['email']
  password = request.json['password']
  
  
  if db_user.find_one({'email': email}):
    #verify if the email already exists
    msg["error_email"] = "El correo ya existe"
    val = False
    
  if db_user.find_one({'username': username}):
    #verify if the username already exists
    msg["error_user"]="El nombre de usuario ya existe"
    val = False
    
  if val == False:
    return error_response(401, msg)
  
  pass_strong = password_check(password)
  
  if pass_strong==True:
    #verify if the password is strong  
    if username and email and password:
      hashed_password = generate_password_hash(password)
      user = User(username, email, hashed_password,' ')
      id = db_user.insert_one(user.toDBCollection()).inserted_id
      response = jsonify({
          'id': str(id),
          'status': 200
      })
      response.status_code = 200
      return response
  
  else:
    return error_response(401, pass_strong)