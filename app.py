from pymongo import MongoClient
import jinja2
from flask import Flask, render_template, jsonify, request,redirect, url_for

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.scheduler

## HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signin' ,methods=['GET'])
def signin():
    return render_template("signin.html")



## api 메소드 -> request.form -> 안받아짐 체크해보기
# user 회원가입.
@app.route('/api/user',methods=['POST'])
def api_signin():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

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
@app.route('/api/name' ,methods=['GET'])
def check_name():
    name = request.args.get('name')
    user = db.users.find_one({"name": name})
    if user is None:
        return jsonify({'msg':'noexist'})
    else:
        return jsonify({'msg':'exist'})


# 계속해서 url변경해주는 부분 확인해보기
@app.route('/api/login' ,methods=['POST'])
def login():
    email=request.form['email']
    password=request.form['password']
    user = db.users.find_one({"email": email})
    if user is None:

        return jsonify({'msg':'noexist'})
    if user['password'] == password:
        return jsonify({'msg':'ok'})
    # url 을 바꿔야하는데

@app.route('/board',methods=['GET'])
def board():
    return render_template('board.html')
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
