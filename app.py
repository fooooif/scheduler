import datetime

from pymongo import MongoClient
from flask_jwt_extended import *
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, jsonify, request,redirect, url_for
from bson import ObjectId
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.update(
    JWT_SECRET_KEY="my_secret_key_jwt",
    JWT_TOKEN_LOCATION='cookies',
    # get post 뺴고 막아놈
    JWT_CSRF_METHODS=["PUT", "PATCH", "DELETE"]
)
jwt = JWTManager(app)

client = MongoClient('localhost', 27017)
db = client.scheduler

day = {1:"월",2:"화",3:"수",4:"목",5:"금",6:"토",7:"일"}
## HTML 화면 보여주기
@app.route('/')
def home():

    return render_template('login2.html')

@app.route('/signin' ,methods=['GET'])
def signin():
    return render_template("signin2.html")

@app.route('/write',methods=['GET'])
@jwt_required()
def write_board():
    jwt_token = get_jwt_identity()
    email = jwt_token['email']
    name = db.users.find_one({'email': email})['name']
    return render_template('write.html',name=name)

@app.route('/board',methods=['GET'])
@jwt_required()
def board():
    jwt_token=get_jwt_identity()
    email = jwt_token['email']
    name = db.users.find_one({'email':email})['name']
    boards = list(db.boards.find({'email': email}))
    for board in boards:
        board['_id']=str(board['_id'])

    return render_template('board.html',name = name,board_list=boards)

## api 메소드 -> request.form -> 안받아짐 체크해보기
# user 회원가입.
@app.route('/api/user',methods=['POST'])
def api_signin():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    password = bcrypt.generate_password_hash(password)
    user = db.users.find_one({"email": email})
    if user is None:
        doc = {
                    "name" : name,
                    "email" : email,
                    "password" : password
        }
        db.users.insert_one(doc)
        return jsonify({'msg':'register'})
    else:
        return jsonify({'msg' :'exist'})

# user name 중복체크 1.requestparam 2.pathvariable
# /api/name?name=""
@app.route('/api/email' ,methods=['GET'])
def check_email():
    email = request.args.get('email')
    user = db.users.find_one({"email": email})
    if user is None:
        return jsonify({'msg':'noexist'})
    else:
        return jsonify({'msg':'exist'})


# 계속해서 url변경해주는 부분 확인해보기
@app.route('/api/login',methods=['POST'])
def login():
    email=request.form['email']
    password=request.form['password']
    user = db.users.find_one({"email":email})

    if user is None:

        return jsonify({'msg':'noexist','access_token':None})

    check = bcrypt.check_password_hash(user['password'],password)

    if check:
        json = {
            'email':email,
        }
        access_token = create_access_token(identity=json,expires_delta=datetime.timedelta(minutes=60))
        return jsonify({'msg':'success','access_token':access_token})
    else:
        return jsonify({'msg':'fail','access_token':None})


@app.route('/api/board',methods=['POST'])
@jwt_required()
def register_board():
    jwt_token = get_jwt_identity()
    email = jwt_token['email']
    json = request.get_json()['data']
    days = []
    for i in json['day']:
        days.append(day[i])
    board_doc = {
        'email':email,
        'day':days,
        'title':json['title'],
        'content':json['content'],
        'time':json['time']
    }
    db.boards.insert_one(board_doc)

    return jsonify({'msg':'succes'})
@app.route('/api/board/drop',methods=['POST'])
@jwt_required()
def delete_board():
    jwt_token = get_jwt_identity()
    json = request.get_json()
    board_ids = json['id']

    for board_id in board_ids:
        db.boards.delete_one({'_id':ObjectId(board_id)})
    return jsonify({'msg':'succes'})

# @app.route('/api/board',methods=['GET'])
# @jwt_required()
# def find_board():
#     jwt_token = get_jwt_identity()
#     email = jwt_token['email']
#
#     boards = list(db.boards.find({'email': email}, {'_id': False}))
#
#     return jsonify({'data':boards})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
