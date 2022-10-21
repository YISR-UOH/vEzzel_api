import requests
import json
from flask import Flask, request, Response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from bson.objectid import ObjectId
from api.user import User
from api.spreadsheet import Spreadsheet



app = Flask(__name__)

url = "https://data.mongodb-api.com/app/data-ysofl/endpoint/data/v1/action/find"

payload = json.dumps({
    "collection": "test",
    "database": "vEzzel",
    "dataSource": "vEzzel",
    "filter": {
      "username":"test1"
    },
    "projection": {
      "password": 0,
    }
    
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'uoLkaRUEQHqg4KHBuxShtiQGuU8o03ls71spzGlSsqgGksV1bWr6EmRKzCsQFd18', 
}

response = requests.request("POST", url, headers=headers, data=payload)
@app.route('/')
def index():
  return response.text

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    