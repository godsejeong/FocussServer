from flask import Flask , render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
from bson import json_util


import json

app = Flask(__name__)

my_client = MongoClient("mongodb://localhost:27017/")
mydb = my_client['focus_flask_api_database']
mycol = mydb['song_data']

def createDB():

    mylist = [
    { "name": "Amy", "address": "Apple st 652"},
    { "name": "Hannah", "address": "Mountain 21"},
    { "name": "Michael", "address": "Valley 345"},
    { "name": "Sandy", "address": "Ocean blvd 2"},
    { "name": "Betty", "address": "Green Grass 1"},
    { "name": "Richard", "address": "Sky st 331"},
    { "name": "Susan", "address": "One way 98"},
    { "name": "Vicky", "address": "Yellow Garden 2"},
    { "name": "Ben", "address": "Park Lane 38"},
    { "name": "William", "address": "Central st 954"},
    { "name": "Chuck", "address": "Main Road 989"},
    { "name": "Viola", "address": "Sideway 1633"}
    ]

    x = mycol.insert_many(mylist)

createDB()

app.config['MONGO_DBNAME'] = 'focusdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/focusdb'

mongo = PyMongo(app)

@app.route("/")
def hello():
    x = dumps(mycol.find({}, {'_id': False}),indent = 4)
    return render_template('index.html',body = x)
    
@app.route("/addSong")
def add():
    

if __name__ == "__main__":              
    app.run(host="127.0.0.1", port="8080")
