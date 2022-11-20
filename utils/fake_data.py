from faker import Faker
from flask import jsonify
import db
from bson.objectid import ObjectId
import random
from werkzeug.security import generate_password_hash
from api.user import User
from api.spreadsheet import Spreadsheet
fake = Faker()

def utils_fake_data():
  '''
    Crea 10 datos falsos para probar
  '''
  db_spreadsheet, db_user, db_comm, db_chats = db.dbconection()
  names = [fake.unique.first_name() for i in range(10)]
  emails = [fake.unique.email() for i in range(10)]
  password = 'Password123'
  ids = []
  tags = ['tag1','tag2','tag3','tag4','tag5','tag6','tag7','tag8','tag9','tag10']
  for i in range(10):
    user = User(names[i], emails[i], generate_password_hash(password),'')
    ids.append(str(db_user.insert_one(user.toDBCollection()).inserted_id))
    
  
  contents = [db_spreadsheet.find_one({'_id':ObjectId("6358180e6aed96bb809df8d4")})["content"],db_spreadsheet.find_one({'_id':ObjectId("63581879d4be9d8a5e95a419")})["content"]]
  
  for j in range(10):
    desc = [fake.unique.sentence(nb_words=10) for _ in range(10)]
    
    tags_spread = [random.sample(tags,random.randint(1,5)) for _ in range(10)]
    content = [random.sample(contents,random.randint(1,1)) for _ in range(10)]
    
    title = [fake.unique.sentence(nb_words=3) for _ in range(10)]
    
    for i in range(10):
      description = desc[i]
      username = names[j]
      spreadsheet = Spreadsheet(str(ids[j]),title[i], description, content[i][0], tags_spread[i], username)
      s_id = db_spreadsheet.insert_one(spreadsheet.toDBCollection()).inserted_id
      
      db_user.update_one({'_id':ObjectId(ids[j])}, {'$set': {'last_sheet': str(s_id)}})
    
  response = jsonify({
      'status': 200      
  })
  response.status_code = 200
  return response