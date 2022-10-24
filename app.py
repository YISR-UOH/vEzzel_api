from distutils.log import error
from email import message
import email
from http import client
from urllib import response
from flask import Flask, request, Response, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import re
from bson.objectid import ObjectId
from api.user import User
from api.spreadsheet import Spreadsheet
from pymongo import MongoClient
import os
from datetime import datetime
from faker import Faker
from flask_cors import CORS
import random


fake = Faker()
app = Flask(__name__)
CORS(app)

#mongodb+srv://vEzzel:v3zzel_Web_Company@vezzel.lgiwpov.mongodb.net/?retryWrites=true&w=majority

MONGO_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGO_URI)
db = client.vEzzel
db_spreadsheet = db['spreadsheet']
db_user = db['test']

sort=list({
    'last_modified': -1
}.items())

def password_check(passwd):
    val = True
    msg = {}
    if len(passwd) < 8: 
        msg['length_min'] = 'La contraseña debe tener al menos 8 caracteres'
        val = False
          
    if not any(char.isdigit() for char in passwd): 
        msg['digit'] = 'La contraseña debe tener al menos un dígito'
        val = False
          
    if not any(char.isupper() for char in passwd): 
        msg['upper'] = 'La contraseña debe tener al menos una letra mayúscula'
        val = False
          
    if not any(char.islower() for char in passwd): 
        msg['lower'] = 'La contraseña debe tener al menos una letra minúscula'
        val = False
        
    if val: 
        return val 
    else:
      return msg

@app.route('/')
def index():
  '''
    Index
  '''
  return render_template('index.html')

@app.route('/getall', methods=['POST'])
def getAll():
  '''
    Lista los usuarios
  '''
  users = []
  for doc in db_user.find():
      users.append({
          '_id': str(ObjectId(doc['_id'])),
          'username': doc['username'],
          'email': doc['email'],
          'password': doc['password']
      })
  return jsonify(users)
  
@app.route('/add', methods=['POST'])
def create_user():
  '''
    Crea un usuario en la base de datos, si no existe ya un usuario con el mismo nombre de usuario o email;
    verifica que la contraseña tenga al menos 8 caracteres, un dígito, una letra mayúscula y una letra minúscula
  '''
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
      user = User(username, email, hashed_password,'')
      id = db_user.insert_one(user.toDBCollection()).inserted_id
      response = jsonify({
          'id': str(id),
          'status': 200
      })
      response.status_code = 200
      return response
  
  else:
    return error_response(401, pass_strong)

@app.route('/edit_user/<id>', methods=['POST'])
def edit_user_name(id):
  '''
    Edita el parametro username del usuario
  '''
  if request.json['username']:
    username = request.json['username']
    if username == db_user.find_one({'_id':  ObjectId(id)})['username']:
      #verify if the username is the same
      return error_response(401, 'El nombre de usuario no puede ser el mismo')
    if username == db_user.find_one({'username': username}):
      #verify if the username already exists
      return error_response(401, 'El nombre de usuario ya existe')
    else:
      db_user.update_one({'_id':ObjectId(id)}, {'$set': {'username': username}})
      msg = 'El nombre de usuario ha sido actualizado'
      
      return good_response(msg)
    
@app.route('/edit_pass/<id>', methods=['POST'])
def edit_user_pass(id):
  '''
    Edita el parametro password del usuario
  '''    
  password = request.json['password']
  if check_password_hash(db_user.find_one({'_id':ObjectId(id)})['password'],password):
    #verify if the password is the same
    return error_response(401,'La contraseña no puede ser la misma')
  pass_strong = password_check(password)
  if pass_strong==True:
    #verify if the password is strong
    hashed_password = generate_password_hash(password)
    db_user.update_one({'_id':ObjectId(id)}, {'$set': {'password': hashed_password}})
    msg = 'La contraseña ha sido actualizada'
    return good_response(msg)
  else:
    return error_response(401, pass_strong) 

@app.route('/edit_email/<id>', methods=['POST'])  
def edit_user_email(id):
  '''
    Edita el parametro email del usuario
  '''    
  email = request.json['email']
  if email == db_user.find_one({'_id':ObjectId(id)})['email']:
    #verify if the email is the same
    return error_response(401,'El correo no puede ser el mismo')
  if email == db_user.find_one({'email': email}): 
    #verify if the email already exists
    return error_response(401, 'El correo ya existe')
  else:
    db_user.update_one({'_id':ObjectId(id)}, {'$set': {'email': email}})
    msg = 'El correo ha sido actualizado'
    return good_response(msg)
  
@app.route("/login", methods=["POST"])
def login():
  '''
    Verifica que el usuario exista y que la contraseña sea correcta
  '''
  email = request.json['email']
  password = request.json['password']
  if db_user.find_one({'email':email}) and check_password_hash(db_user.find_one({'email':email})['password'],password):
    #verify if the email and password are correct
    id = db_user.find_one({'email':email})['_id']
    response = jsonify({'id': str(id),'status': 200})
    response.status_code = 200
    return response
  
  else:
    return error_response(401, 'Usuario o contraseña incorrectos')

@app.route('/spreadsheet/<id>', methods=['POST'])
def getSpreadsheet(id):
  '''
    Retorna las Spreadsheet del usuario
  '''
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    spreadsheet = db_spreadsheet.find(filter={'user_id':id},sort=sort)
    response = []
    for s in spreadsheet:
      response.append({
          '_id': str(s['_id']),
          'name': s['name'],
          'user_id': s['user_id'],
          'description': s['description'],
          'content': s['content'],
          'tags': s['tags'],
          'username': s['username'],
          'last_modified': s['last_modified']
      })
    response = jsonify(response)
    response.status_code = 200
    return response
  return error_response(401, 'El usuario no tiene Spreadsheet')
  
@app.route('/spreadsheet_save/<id>', methods=['POST'])
def saveSpreadsheet(id):
  '''
    Guarda un Spreadsheet
  '''
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    name = request.json['name']
    description = request.json['description']
    content = request.json['content']
    tags = request.json['tags']
    username = db_user.find_one({'_id':ObjectId(id)})['username']
    
    spreadsheet = Spreadsheet(str(id),name, description, content, tags, username)
    s_id = db_spreadsheet.insert_one(spreadsheet.toDBCollection()).inserted_id
    
    db_user.update_one({'_id':ObjectId(id)}, {'$set': {'last_modified': str(s_id)}})
    
    msg = 'El Spreadsheet ha sido guardado'
    return good_response(msg)
  return error_response(401, 'El usuario no existe')

@app.route('/spreadsheet_edit/<id>/<spread_id>', methods=['POST'])
def editSpreadsheet(id, spread_id):
  '''
    Edita un spreadsheet
  '''
  
  if db_user.find_one({'_id':ObjectId(id)}):
    if db_spreadsheet.find_one({'_id':ObjectId(spread_id), 'user_id':str(id)}):
      #verify if the user and spreadsheet exists
      name = request.json['name']
      description = request.json['description']
      content = request.json['content']
      tags = request.json['tags']
      now = datetime.now()
      date_time = now.strftime("%Y%m%d%H%M%S")
      db_spreadsheet.update_one({'_id':ObjectId(spread_id)}, {'$set': {'name': name, 'description': description, 'content': content, 'tags': tags, "last_modified": date_time}})
      
      db_user.update_one({'_id':ObjectId(id)}, {'$set': {'last_modified': str(spread_id)}})
      
      return good_response('El Spreadsheet ha sido actualizado')
    else:
      return error_response(401, 'El Spreadsheet no existe')
  
  else:
    return error_response(401, 'El usuario no existe')


@app.route('/spreadsheet_delete/<id>/<spread_id>', methods=['POST'])
def deleteSpreadsheet(id, spread_id):
  '''
    Elimina un spreadsheet
  '''
  
  if db_user.find_one({'_id':ObjectId(id)}):
    if db_spreadsheet.find_one({'_id':ObjectId(spread_id), 'user_id':str(id)}):
      #verify if the user and spreadsheet exists
      db_spreadsheet.delete_one({'_id':ObjectId(spread_id)})
      
      if db_user.find_one({'_id':ObjectId(id)})['last_modified'] == str(spread_id):
        db_user.update_one({'_id':ObjectId(id)}, {'$set': {'last_modified': ''}})
      
      msg = 'El Spreadsheet ha sido eliminado'
      return good_response(msg)
    else:
      return error_response(401, 'El Spreadsheet no existe')
  
  else:
    return error_response(401, 'El usuario no existe')

@app.route('/spreadsheet_search', methods=['POST'])
def searchSpreadsheet_name():
  '''
    Busca un spreadsheet por nombre y/o tags
  '''
  name,tags = False,False
  #tiene que devolver todo por default
  response = []
  spreadsheet = 0
  if 'name' in request.json:
    #verify if recive the name
    name = request.json['name']
  
  if 'tags' in request.json:
    #verify if recive the tags
    tags = request.json['tags']
    
  if name != False and tags == False:
    spreadsheet = db_spreadsheet.find(
      filter={'name': {
        '$regex': name, 
        '$options': 'i'
    }},
      sort=sort
    )
    
  elif name == False and tags != False:
    spreadsheet = db_spreadsheet.find(
      filter={'tags':{
        '$all':[re.compile(i,re.IGNORECASE) for i in tags]  
        }},
      sort=sort
    )

  elif name != False and tags != False:
    spreadsheet = db_spreadsheet.find(
      filter={
        'name': re.compile(name, re.IGNORECASE),
        'tags':{
        '$all':[re.compile(i,re.IGNORECASE) for i in tags]  
        }},
      sort=sort
    )
  
  elif name == False and tags == False:
    spreadsheet = db_spreadsheet.find(
      filter={},
      sort=sort
    )
  
  if spreadsheet != 0:
    for s in spreadsheet:
      response.append({
          '_id': str(s['_id']),
          'name': s['name'],
          'user_id': s['user_id'],
          'description': s['description'],
          'content': s['content'],
          'tags': s['tags'],
          'username': s['username'],
          "last_modified":str(s["last_modified"])
      })

  response = jsonify(response)
  response.status_code = 200
  return response

@app.route('/spreadsheet_getlast/<id>', methods=['POST'])
def getLastSpreadsheet(id):
  '''
    Obtiene el último spreadsheet modificado
  '''
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    last_modified = db_user.find_one({'_id':ObjectId(id)})['last_sheet']
    if last_modified != '':
      spreadsheet = db_spreadsheet.find_one({'_id':ObjectId(last_modified)})
      response = {
          '_id': str(spreadsheet['_id']),
          'name': spreadsheet['name'],
          'user_id': spreadsheet['user_id'],
          'description': spreadsheet['description'],
          'content': spreadsheet['content'],
          'tags': spreadsheet['tags'],
          'username': spreadsheet['username'],
          'last_modified': spreadsheet['last_modified']
      }
      response = jsonify(response)
      response.status_code = 200
      return response
    else:
      return error_response(401, 'El usuario no tiene un Spreadsheet modificado')
  return error_response(401, 'El usuario no existe')
  

def error_response(error,msg):
  '''
    Error 401 - Unauthorized Access 
  '''
  message = {
      'status': error,
      'message': msg
  }
  resp = jsonify(message)
  resp.status_code = error

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


@app.route('/spreadsheet_random', methods=['POST'])
def fake_data():
  '''
    Crea 10 datos falsos para probar
  '''
  names = [fake.unique.first_name() for i in range(10)]
  emails = [fake.unique.email() for i in range(10)]
  password = 'Password123'
  ids = []
  tags = ['tag1','tag2','tag3','tag4','tag5','tag6','tag7','tag8','tag9','tag10']
  for i in range(10):
    user = User(names[i], emails[i], generate_password_hash(password),'')
    ids.append(str(db_user.insert_one(user.toDBCollection()).inserted_id))
    
  

  for j in range(10):
    desc = [fake.unique.sentence(nb_words=10) for _ in range(10)]
    
    tags_spread = [random.sample(tags,random.randint(1,5)) for _ in range(10)]
    content = ' '
    title = [fake.unique.sentence(nb_words=3) for _ in range(10)]
    
    for i in range(10):
      description = desc[i]
      username = names[j]
      spreadsheet = Spreadsheet(str(ids[j]),title[i], description, content, tags_spread[i], username)
      s_id = db_spreadsheet.insert_one(spreadsheet.toDBCollection()).inserted_id
      
      db_user.update_one({'_id':ObjectId(ids[j])}, {'$set': {'last_sheet': str(s_id)}})
    
  response = jsonify({
      'status': 200      
  })
  response.status_code = 200
  return response
  
if __name__ == '__main__':
    app.run(threaded=True, port=5000)

