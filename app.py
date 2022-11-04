from flask import Flask, render_template
import os
from flask_cors import CORS

from utils.fake_data import utils_fake_data

from users.getAll import users_getAll
from users.create_user import users_create_user
from users.edit_user_name import users_edit_user_name
from users.edit_user_pass import users_edit_user_pass
from users.edit_user_email import users_edit_user_email
from users.login import users_login

from spread.getSpread import spread_getSpreadsheet
from spread.editSpreadsheet import spread_editSpreadsheet
from spread.saveSpreadsheet import spread_saveSpreadsheet
from spread.deleteSpreadsheet import spread_deleteSpreadsheet
from spread.searchSpreadsheet_name import spread_searchSpreadsheet_name
from spread.getLastSpreadsheet import spread_getLastSpreadsheet


app = Flask(__name__)
CORS(app)

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


# Ruta para generar datos falsos
@app.route('/spreadsheet_random', methods=['POST'])
def fake_data(): return utils_fake_data()


if __name__ == '__main__':
  app.run(threaded=True, port=5000)
  

