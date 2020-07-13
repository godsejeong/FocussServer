
# -*- coding: utf-8 -*- 

from flask import Flask,render_template ,request ,send_from_directory
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
from werkzeug.utils import secure_filename

import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

my_client = MongoClient("mongodb://localhost:27017/")
mydb = my_client['focus_flask_api_database']
song_col = mydb['song_data']
category_col = mydb['category_data']
sub_category_col = mydb['sub_category_data']
tag_col = mydb['tag_data']

def createDB():
    
    mycategory = [
        {'name' : "ASMR"},
        {'name' : "백색소음"},
        {'name' : "파아노"}
    ];
    
    mysubcategory = [
        {'name' : "자연"},
        {'name' : "공부"},
        {'name' : "가요"},
        {'name' : "OST"}
    ];

    mystag = [
        {'name' : "슬픔"},
        {'name' : "감동"},
        {'name' : "평화"},
        {'name' : "애절"},
        {'name' : "신남"},
        {'name' : "우울"},
        {'name' : "신비"},
        {'name' : "잔잔"},
        {'name' : "즐거움"},
        {'name' : "일상"},
        {'name' : "활기"},
        {'name' : "행복"},
        {'name' : "경쾌"},
        {'name' : "시원"},
    ];
    
    category_col.insert_many(mycategory)
    sub_category_col.insert_many(mysubcategory)
    tag_col.insert_many(mystag)

def deleteDB():
    song_col.drop()
    category_col.drop()
    sub_category_col.drop()
    tag_col.drop()
    
# deleteDB()

app.config['MONGO_DBNAME'] = 'focusdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/focusdb'

mongo = PyMongo(app)

@app.route("/")
def hello():
    output = []
    for value in category_col.find():
        output.append({'name' : value['name']})
    return render_template('index.html',category_data = output)

@app.route("/list")
def list_post():
    output = []
    for value in song_col.find():
        output.append({'name' : value['name'],'artist' : value['artist'],'literaryProperty' : value['literaryProperty'],
        'thumbnail' : value['thumbnail'],'music' : value['music'],'category' : value['category'],'sub' : value['sub'],'tag' : value['tag']})
    return render_template('list.html',song = {'result' : output})    

@app.route("/sub")
def popup_sub():
    output = []
    for value in sub_category_col.find():
        output.append({'name' : value['name']})
    return render_template('popup.html',popup_data = {'result' : output})


@app.route("/tag")
def popup_tag():
    output = []
    for value in tag_col.find():
        output.append({'name' : value['name']})
    return render_template('popup.html',popup_data = {'result' : output})

@app.route("/tagadd")
def add_tag_page():
    return render_template('add.html',add = "tag")


@app.route("/subadd")
def add_sub_page():
    return render_template('add.html',add = "sub")

@app.route("/uploadTag",methods =['POST'])
def tag_post():
    try:
        tag_value = request.form['tag']

        colis = False
        for value in tag_col.find():
            if(tag_value == value['name']):
                colis = False
            else:
                colis = True
            

        if(colis):
            print(tag_value)
            tag_item = {'name' : tag_value},
            tag_col.insert_many(tag_item)
            return {'StatusCode': '200', 'Message': '입력하신 태그가 추가되었습니다.'}
        else:
            return {'StatusCode': '403', 'Message': '태그내용이 이미 존재합니다!!'}
    except Exception as e:
        return {'StatusCode': '400', 'Message': str(e)}

@app.route("/uploadSub",methods =['POST'])
def sub_post():
    try:
        sub_value = request.form['sub']

        colis = False
        for value in sub_category_col.find():
            if(sub_value == value['name']):
                colis = False
            else:
                colis = True

        if(colis):
            print(sub_value)
            sub_item = {'name' : sub_value},
            sub_category_col.insert_many(sub_item)
            return {'StatusCode': '200', 'Message': '입력하신 서브항목이 추가되었습니다.'}
        else:
            return {'StatusCode': '403', 'Message': '서브 항목이 이미 존재합니다!!'}
    except Exception as e:
        return {'StatusCode': '400', 'Message': str(e)}     

@app.route("/removeSub",methods =['POST'])
def remote_sub_post():
    try:
        sub_value = request.form.getlist('sub[]')

        for sub_list in sub_value:
            for value in sub_category_col.find():
                if(sub_list == value['name']):
                    delete_col = {'name' : sub_list}
                    sub_category_col.delete_one(delete_col)    

        return {'StatusCode': '200', 'Message': '삭제되었습니다.'}
    
    except Exception as e:
        return {'StatusCode': '400', 'Message': str(e)}

@app.route("/removeTag",methods =['POST'])
def remote_tag_post():
    try:
        tag_value = request.form.getlist('tag[]')

        for tag_list in tag_value:
            for value in tag_col.find():
                if(tag_list == value['name']):
                    delete_col = {'name' : tag_list}
                    tag_col.delete_one(delete_col)    

        return {'StatusCode': '200', 'Message': '삭제되었습니다.'}
    
    except Exception as e:
        return {'StatusCode': '400', 'Message': str(e)}

@app.route('/thumbnails/<path:filename>', methods=['GET', 'POST'])
def thumbnails_download(filename):
    return send_from_directory(directory='./uploads/thumbnails/', filename=filename)

@app.route('/songs/<path:filename>', methods=['GET', 'POST'])
def songs_download(filename):
    return send_from_directory(directory='./uploads/songs/', filename=filename)            

@app.route("/removeSong",methods = ['POST'])
def remove_song_post():
    try:
        name = request.form['name']
        delete_col = {'name' : name}
        song_col.delete_one(delete_col)
        return {'StatusCode': '200', 'Message': '삭제되었습니다.'}
    except Exception as e:
        return {'StatusCode': '400', 'Message': str(e)}

@app.route("/uploadSong",methods = ['POST'])
def upload_song_post():
    try:
        name = request.form['name']  #이름 String
        artist = request.form['artist']  #아티스트 String
        literaryProperty = request.form['literaryProperty']   #저작권 String
        thumbnail = request.files['thumbnail']   #썸네일 Fils
        music = request.files['music']   #음악 Fils
        category = request.form['category'] #항목 String
        sub = request.form['sub'] #서브항목 List
        tag = request.form['tag'] #태그 List

        thumbnail.save('./uploads/thumbnails/' + secure_filename(thumbnail.filename))
        music.save('./uploads/songs/' + secure_filename(music.filename))

        tagList = tag.strip().split(' ')
        subList = sub.strip().split(' ')

        #이름,음악 파일명,썸네일 파일명
        nameis = False
        thumbnailis = False
        musicis = False

        for value in song_col.find():
            if(name == value['name']):
                nameis = True
            else:
                nameis = False

            if(thumbnail.filename == value['thumbnail']):
                thumbnailis = True
            else:
                thumbnailis = False

            if(music.filename == value['music']):
                musicis = True
            else:
                musicis = False


        song = [{'name' : name , 'artist' : artist , 'literaryProperty' : literaryProperty ,
         'thumbnail' : thumbnail.filename , 'music' : music.filename , 'category' : category , 'sub' : subList, 'tag' : tagList}]


        if(nameis):
            return {'StatusCode': '403', 'Message': '이름이 이미 존재합니다.'}
        elif(thumbnailis):
            return {'StatusCode': '403', 'Message': '썸네일명이 이미 존재합니다.'}
        elif(musicis):
            return {'StatusCode': '403', 'Message': '음악명이 이미 존재합니다.'}
        else:
            song_col.insert_many(song)
            return {'StatusCode': '200', 'Message': '정상적으로 처리되었습니다.'}

    except Exception as e:
        return {'StatusCode': '400', 'Message': str(e)}

class UploadSong(Resource):
    def post(self):
        return {'status': 'success'}

class GetAllList(Resource):
    def post(self):
        return {'status' : 'success'}        

api.add_resource(UploadSong, '/upload')
api.add_resource(GetAllList, '/all')
# api.add_resource(GetAllList, '/addTag')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80",debug=True)
