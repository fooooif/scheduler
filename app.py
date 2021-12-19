import datetime

from pymongo import MongoClient
import jinja2
from flask_jwt_extended import *
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, jsonify, request,redirect, url_for

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY="my_secret_key_jwt",
    JWT_TOKEN_LOCATION='cookies'
)
jwt = JWTManager(app)

client = MongoClient('localhost', 27017)
db = client.scheduler

## HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('login2.html')

@app.route('/signin' ,methods=['GET'])
def signin():
    return render_template("signin2.html")



## api 메소드 -> request.form -> 안받아짐 체크해보기
# user 회원가입.
@app.route('/api/user',methods=['POST'])
def api_signin():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    password = bcrypt.generate_password_hash(password)
    print(password)
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
    print(email)
    user = db.users.find_one({"email": email})
    if user is None:
        return jsonify({'msg':'noexist'})
    else:
        return jsonify({'msg':'exist'})


# 계속해서 url변경해주는 부분 확인해보기
@app.route('/api/login' ,methods=['POST'])
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
        access_token = create_access_token(identity=json,expires_delta=datetime.timedelta(minutes=15))
        return jsonify({'msg':'success','access_token':access_token})
    else:
        return jsonify({'msg':'fail','access_token':None})


@app.route('/board',methods=['GET'])
@jwt_required()
def board():
    print(request.headers)
    return render_template('board.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
