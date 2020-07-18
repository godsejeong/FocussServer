
# -*- coding: utf-8 -*- 

from flask import Flask,render_template ,request ,send_from_directory
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
from werkzeug.utils import secure_filename
import os

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
    return render_template('index.html',fix_col = {"result" : ""})

@app.route("/list")
def list_post():
    output = []
    for value in song_col.find():
        output.append({'name' : value['name'],'artist' : value['artist'],'literaryProperty' : value['literaryProperty'],'hash' : value['hash'],
        'thumbnail' : value['thumbnail'],'music' : value['music'],'category' : value['category'],'sub' : value['sub'],'tag' : value['tag']})
    return render_template('list.html',song = {'result' : output})    

@app.route("/sub")
def popup_sub():
    output = []
    for value in sub_category_col.find():
        output.append({'name' : value['name']})
    return render_template('popup.html',popup_data = {'result' : output})

@app.route("/fix/<path:name>",methods=['GET', 'POST'])
def fix_post(name):
    output = []
    name_col = {'name' : name}
    find_col = song_col.find(name_col)

    for value in find_col:
        output.append({'name' : value['name'],'artist' : value['artist'],'literaryProperty' : value['literaryProperty'],'hash' : value['hash'],
        'category' : value['category'],'sub' : value['sub'],'tag' : value['tag']})

    return render_template('index.html',fix_col = {"result" : output})

@app.route("/tag")
def popup_tag():
    output = []
    for value in tag_col.find():
        output.append({'name' : value['name']})
    return render_template('popup.html',popup_data = {'result' : output})

@app.route("/category")
def popup_category_col():
    output = []
    for value in category_col.find():
        output.append({'name' : value['name']})
    return render_template('popup.html',popup_data = {'result' : output})    

@app.route("/tagadd")
def add_tag_page():
    return render_template('add.html',add = "tag")

@app.route("/subadd")
def add_sub_page():
    return render_template('add.html',add = "sub")

@app.route("/categoryadd")
def add_category():
    return render_template('add.html',add = "category")    

@app.route("/uploadTag",methods =['POST'])
def tag_post():
    try:
        tag_value = request.form['tag']

        colis = True
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

        colis = True
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

@app.route("/uploadCategory",methods =['POST'])
def category_post():
    try:
        category_value = request.form['category']

        colis = True
        for value in category_col.find():
            if(category_value == value['name']):
                colis = False
            else:
                colis = True

        if(colis):
            print(category_value)
            category_item = {'name' : category_value},
            category_col.insert_many(category_item)
            return {'StatusCode': '200', 'Message': '입력하신 항목이 추가되었습니다.'}
        else:
            return {'StatusCode': '403', 'Message': '항목이 이미 존재합니다!!'}
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

@app.route("/removeCategory",methods =['POST'])
def remote_category_post():
    try:
        category_value = request.form.getlist('category[]')

        for category_list in category_value:
            for value in category_col.find():
                if(category_list == value['name']):
                    delete_col = {'name' : category_list}
                    category_col.delete_one(delete_col)    

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

        songlist = song_col.find(delete_col)

        print(songlist)

        for x in songlist:
            music = x['music']
            thumbnail = x['thumbnail']
            os.remove("./uploads/thumbnails/"+thumbnail)
            os.remove("./uploads/songs/"+music)
            
        song_col.delete_one(delete_col)
        return {'StatusCode': '200', 'Message': '삭제되었습니다.'}
    except Exception as e:
        return {'StatusCode': '400', 'Message': str(e)}

@app.route("/fixSong",methods = ['POST'])
def fix_song_post():
    # try:

        original_name = request.form['original_name']  #이름 String

        print(original_name)

        name = request.form['name']  #이름 String
        artist = request.form['artist']  #아티스트 String
        literaryProperty = request.form['literaryProperty']   #저작권 String
        category = request.form['category'] #항목 String
        thumbnail = request.files.get('thumbnail')   #썸네일 Fils
        music = request.files.get('music')   #음악 Fils
        sub = request.form['sub'] #서브항목 List
        tag = request.form['tag'] #태그 List
        _hash = request.form['hash'] #해쉬태그 String

        tagList = tag.strip().split(' ')
        subList = sub.strip().split(' ')

        name_col = {'name' : original_name}
        find_col = song_col.find(name_col)

        newvalues = {}
        
        # print("a" + thumbnail)

        # print("b" + music)

        if(thumbnail and music):
             print('thumbnail and music')
             newvalues = { "$set": {'name' : name , 'artist' : artist , 'literaryProperty' : literaryProperty ,"hash" : _hash,
             'thumbnail' : secure_filename(thumbnail.filename) , 'music' : secure_filename(music.filename), 'category' : category,
             'sub' : subList, 'tag' : tagList} }
        elif(thumbnail):
             print('thumbnail')
             newvalues = { "$set": {'name' : name , 'artist' : artist , 'literaryProperty' : literaryProperty ,"hash" : _hash,
             'thumbnail' : secure_filename(thumbnail.filename) , 'category' : category,'sub' : subList, 'tag' : tagList} }
        elif(music):
             print('music')
             newvalues = { "$set": {'name' : name , 'artist' : artist , 'literaryProperty' : literaryProperty ,"hash" : _hash,
             'music' : secure_filename(music.filename), 'category' : category,'sub' : subList, 'tag' : tagList} }
        else:
             print('not print')
             newvalues = { "$set": {'name' : name , 'artist' : artist , 'literaryProperty' : literaryProperty ,"hash" : _hash,
            'category' : category,'sub' : subList, 'tag' : tagList} }

        nameis = False
        musicis = False
        thumbnailis = False

        for value in song_col.find():
            if(name == value['name']):
                nameis = True
            else:
                nameis = False

        for value in song_col.find():
            try: 
                if(secure_filename(music.filename) == value['music']):
                    nameis = True
                else:
                    nameis = False
            except:
                nameis = False
                print("not Music")

        for value in song_col.find():
            try:
                if(secure_filename(thumbnail.filename) == value['thumbnail']):
                    thumbnailis = True
                else:
                    thumbnailis = False
            except:
                thumbnailis = False
                print('not Thumbanilis')

        if(name == original_name):
            nameis = False

        if(nameis):
            return {'StatusCode': '403', 'Message': '이름이 이미 존재합니다.'}
        elif(thumbnailis):
            return {'StatusCode': '403', 'Message': '썸네일 파일명이 이미 존재합니다.'}
        elif(musicis):
            return {'StatusCode': '403', 'Message': '음악 파일명이 이미 존재합니다.'}
        else:
            song_col.update_one(name_col,newvalues)
            return {'StatusCode': '200', 'Message': '정상적으로 처리되었습니다.'}

    # except Exception as e:
    #     return {'StatusCode': '400', 'Message': str(e)}


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
        _hash = request.form['hash'] #해쉬태그 String

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


        song = [{'name' : name , 'artist' : artist , 'literaryProperty' : literaryProperty ,"hash" : _hash,
         'thumbnail' : secure_filename(thumbnail.filename) , 'music' : secure_filename(music.filename),
         'category' : category , 'sub' : subList, 'tag' : tagList}]


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

class getCategory(Resource):
    def post(self):
        try:
            output = []
            for value in category_col.find():
                output.append({'name' : value['name']})
            return {'StatusCode': '200', 'Result': output}
        except Exception as e:
            return {'StatusCode': '400', 'Message': str(e)}

# class UploadSong(Resource):
#     def post(self):
#         return {'status': 'success'}

# class GetAllList(Resource):
#     def post(self):
#         return {'status' : 'success'}        

# api.add_resource(UploadSong, '/upload')
# api.add_resource(GetAllList, '/all')
api.add_resource(getCategory, '/getCategory')
# api.add_resource(GetAllList, '/addTag')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080",debug=True)
