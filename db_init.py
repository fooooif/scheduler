from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.scheduler


def db_users():
    user_doc = {
        "name": "",
        "email": "",
        "password": "",
    }
    db.users.insert_one(user_doc)


def db_board():
    board_doc = {
        "user_name": "",
        "password": "",
        "title": "",
        "content":""
    }
    db.boards.insert_one(board_doc)
