from flask import Flask, render_template, request,jsonify
from flask_cors import CORS

from utils.fake_data import utils_fake_data

from users.getAll import users_getAll
from users.create_user import users_create_user
from users.edit_user_name import users_edit_user_name
from users.edit_user_pass import users_edit_user_pass
from users.edit_user_email import users_edit_user_email
from users.login import users_login
from users.deleteUser import users_deleteUser

from spread.getSpread import spread_getSpreadsheet
from spread.editSpreadsheet import spread_editSpreadsheet
from spread.saveSpreadsheet import spread_saveSpreadsheet
from spread.deleteSpreadsheet import spread_deleteSpreadsheet
from spread.searchSpreadsheet_name import spread_searchSpreadsheet_name
from spread.getLastSpreadsheet import spread_getLastSpreadsheet
from spread.getOneSpread import spread_getOneSpread
from comments.createComm import com_createComm
from comments.deleteComm import com_deleteComm
from comments.editComm import com_editComm
from comments.getSpreadComm import com_getSpreadComm 
from comments.getUserComm import com_getUserComm
from comments.getUserSpreadComm import com_getUserSpreadComm

from chat.getAllChat import chat_getAllChat
from chat.saveChat import chat_saveChat
from chat.createChat import chat_createChat
from flask_socketio import SocketIO,emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


# Pagina de inicio
@app.route('/')
def index():
  '''
    Index
  '''
  return render_template('index.html')


# Rutas de usuarios
@app.route('/getall', methods=['POST'])
def getAll():return users_getAll()

@app.route('/add', methods=['POST'])
def create_user(): return users_create_user()

@app.route('/edit_user/<id>', methods=['POST'])
def edit_user_name(id): return users_edit_user_name(id)
    
@app.route('/edit_pass/<id>', methods=['POST'])
def edit_user_pass(id): return users_edit_user_pass(id)

@app.route('/edit_email/<id>', methods=['POST'])  
def edit_user_email(id): return users_edit_user_email(id)
  
@app.route("/login", methods=["POST"])
def login():return users_login()

@app.route('/deleteUser/<id>', methods=['POST'])
def deleteUser(id):return users_deleteUser(id)



# rutas de spreadsheets
@app.route('/spreadsheet/<id>', methods=['POST'])
def getSpreadsheet(id): return spread_getSpreadsheet(id)
  
@app.route('/spreadsheet_save/<id>', methods=['POST'])
def saveSpreadsheet(id): return spread_saveSpreadsheet(id)

@app.route('/spreadsheet_edit/<id>/<spread_id>', methods=['POST'])
def editSpreadsheet(id, spread_id): return spread_editSpreadsheet(id, spread_id)

@app.route('/spreadsheet_delete/<id>/<spread_id>', methods=['POST'])
def deleteSpreadsheet(id, spread_id):return spread_deleteSpreadsheet(id, spread_id)

@app.route('/spreadsheet_search', methods=['POST'])
def searchSpreadsheet_name(): return spread_searchSpreadsheet_name()

@app.route('/spreadsheet_getlast/<id>', methods=['POST'])
def getLastSpreadsheet(id):return spread_getLastSpreadsheet(id)

@app.route('/getOneSpread/<spread_id>', methods=['POST'])
def getOneSpread(spread_id):return spread_getOneSpread(spread_id)




# rutas de comentarios
@app.route('/createComm/<id>/<spread_id>', methods=['POST'])
def createComm(id, spread_id): return com_createComm(id, spread_id)

@app.route('/deleteComm/<id>/<spread_id>/<comm_id>', methods=['POST'])
def deleteComm(id, spread_id, comm_id): return com_deleteComm(id, spread_id, comm_id)

@app.route('/editComm/<id>/<spread_id>/<comm_id>', methods=['POST'])
def editComm(id, spread_id, comm_id): return com_editComm(id, spread_id, comm_id)

@app.route('/getSpreadComm/<spread_id>', methods=['POST'])
def getSpreadComm(spread_id): return com_getSpreadComm(spread_id)

@app.route('/getUserComm/<id>', methods=['POST'])
def getUserComm(id): return com_getUserComm(id)

@app.route('/getUserSpreadComm/<id>/<spread_id>', methods=['POST'])
def getUserSpreadComm(id, spread_id): return com_getUserSpreadComm(id, spread_id)




# rutas de chat
@app.route('/getAllChat', methods=['POST'])
def getAllChat(): return chat_getAllChat()

@app.route('/saveChat', methods=['POST'])
def saveChat(): return chat_saveChat()

@app.route('/createChat', methods=['POST'])
def createChat(): return chat_createChat()
@socketio.on('connection')
def chat_connection(data):
    """event listener when client connects to the server"""
    
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})
    
@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    chat_saveChat(data)
    emit("data",{'data':data,'id':request.sid},broadcast=True)
    
@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

if __name__ == '__main__':
  socketio.run(app,debug=True, port=5000)
  

