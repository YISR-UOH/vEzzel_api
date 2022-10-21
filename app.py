from http import client
from flask import Flask, request, Response, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash

from bson.objectid import ObjectId
from api.user import User
from api.spreadsheet import Spreadsheet
from pymongo import MongoClient
import os


app = Flask(__name__)
MONGO_URI = os.getenv("MONGODB_URI")
print(MONGO_URI)
client = MongoClient(MONGO_URI)
db = client.vEzzel
db_spreadsheet = db['spreadsheet']
db_user = db['test']


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
  return '<h1>vEzzel API</h1>'

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
    
  if db_user.find_one({'username': username}):
    #verify if the username already exists
    msg["error_user"]="El nombre de usuario ya existe"
    
  if val == False:
    return jsonify(msg)
  
  pass_strong = password_check(password)
  
  if pass_strong==True:
    #verify if the password is strong  
    if username and email and password:
      hashed_password = generate_password_hash(password)
      user = User(username, email, hashed_password)
      id = db_user.insert_one(user.toDBCollection()).inserted_id
      response = jsonify({
          '_id': str(id),
          'username': username,
          'password': password,
          'email': email
      })
      response.status_code = 201
    return response
  
  else:
    return jsonify(pass_strong)

@app.route('/edit_user/<id>', methods=['POST'])
def edit_user_name(id):
  '''
    Edita el parametro username del usuario
  '''
  if request.json['username']:
    username = request.json['username']
    if username == db_user.find_one({'_id':  ObjectId(id)})['username']:
      #verify if the username is the same
      return jsonify({'message': 'El nombre de usuario no puede ser el mismo'})
    if username == db_user.find_one({'username': username}):
      #verify if the username already exists
      return jsonify({'message': 'El nombre de usuario ya existe'})
    else:
      db_user.update_one({'_id':ObjectId(id)}, {'$set': {'username': username}})
      return jsonify({'message': 'El nombre de usuario ha sido actualizado'})
    
@app.route('/edit_pass/<id>', methods=['POST'])
def edit_user_pass(id):
  '''
    Edita el parametro password del usuario
  '''    
  password = request.json['password']
  if check_password_hash(db_user.find_one({'_id':ObjectId(id)})['password'],password):
    #verify if the password is the same
    return jsonify({'message': 'La contraseña no puede ser la misma'})
  pass_strong = password_check(password)
  if pass_strong==True:
    #verify if the password is strong
    hashed_password = generate_password_hash(password)
    db_user.update_one({'_id':ObjectId(id)}, {'$set': {'password': hashed_password}})
    return jsonify({'message': 'La contraseña ha sido actualizada'})
  else:
    return jsonify({'message': pass_strong}) 


@app.route('/edit_email/<id>', methods=['POST'])  
def edit_user_email(id):
  '''
    Edita el parametro email del usuario
  '''    
  email = request.json['email']
  if email == db_user.find_one({'_id':ObjectId(id)})['email']:
    #verify if the email is the same
    return jsonify({'message': 'El correo no puede ser el mismo'})
  if email == db_user.find_one({'email': email}): 
    #verify if the email already exists
    return jsonify({'message': 'El correo ya existe'})
  else:
    db_user.update_one({'_id':ObjectId(id)}, {'$set': {'email': email}})
    return jsonify({'message': 'El correo ha sido actualizado'})
  
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
    return jsonify({'id': str(id)})
  
  else:
    return jsonify({'message': 'El correo o la contraseña son incorrectos'})

@app.route('/spreadsheet/<id>', methods=['POST'])
def getSpreadsheet(id):
  '''
    Retorna los Spreadsheet del usuario
  '''
  if db_user.find_one({'_id':ObjectId(id)}):
    #verify if the user exists
    spreadsheet = db_spreadsheet.find({'user_id':id})
    response = []
    for s in spreadsheet:
      response.append({
          '_id': str(s['_id']),
          'name': s['name'],
          'user_id': s['user_id'],
          'description': s['description'],
          'content': s['content'],
          'tags': s['tags'],
          'tracker': s['tracker']
      })
      
    return jsonify(response)
  return jsonify({'message': 'El usuario no tiene Spreadsheet'})
  
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
    tracker = request.json['tracker']
    
    spreadsheet = Spreadsheet(str(id),name, description, content, tags, tracker)
    s_id = db_spreadsheet.insert_one(spreadsheet.toDBCollection()).inserted_id
    
    response = jsonify({
        '_id': str(s_id),
        'name': name,
        'user_id': str(id),
        'description': description,
        'content': content,
        'tags': tags,
        'tracker': tracker
    })
    response.status_code = 201
    return response
  return jsonify({'message': 'El usuario no existe'})

@app.route('/spreadsheet_edit/<id>/<spread_id>', methods=['POST'])
def editSpreadsheet(id, spread_id):
  '''
    Edita un spreadsheet
  '''
  
  if db_user.find_one({'_id':ObjectId(id)}):
    if db_spreadsheet.find_one({'_id':ObjectId(spread_id), 'user_id':ObjectId(id)}):
      #verify if the user and spreadsheet exists
      name = request.json['name']
      description = request.json['description']
      content = request.json['content']
      tags = request.json['tags']
      
      db_spreadsheet.update_one({'_id':ObjectId(spread_id)}, {'$set': {'name': name, 'description': description, 'content': content, 'tags': tags}})
      
      
      return jsonify({'message': 'El Spreadsheet ha sido actualizado'})
    else:
      return jsonify({'message': 'El Spreadsheet no existe'})
  
  else:
    return jsonify({'message': 'El usuario no existe'})


@app.route('/spreadsheet_delete/<id>/<spread_id>', methods=['POST'])
def deleteSpreadsheet(id, spread_id):
  '''
    Elimina un spreadsheet
  '''
  
  if db_user.find_one({'_id':ObjectId(id)}):
    if db_spreadsheet.find_one({'_id':ObjectId(spread_id), 'user_id':ObjectId(id)}):
      #verify if the user and spreadsheet exists
      db_spreadsheet.delete_one({'_id':ObjectId(spread_id)})
      return jsonify({'message': 'El Spreadsheet ha sido eliminado'})
    else:
      return jsonify({'message': 'El Spreadsheet no existe'})
  
  else:
    return jsonify({'message': 'El usuario no existe'})



if __name__ == '__main__':
    app.run(threaded=True, port=5000)
    