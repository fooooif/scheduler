from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.scheduler


#
# def db_users():
#     user_doc = {
#         "name": "",
#         "email": "",
#         "password": "",
#     }
#     db.users.insert_one(user_doc)
#
#
# def db_board():
#     board_doc = {
#         'email':"",
#         'day': [],
#         'title': "",
#         'content': "",
#         'time': ""
#     }
#     db.boards.insert_one(board_doc)
#
#
# # 저장 - 예시
# doc = {'name':'bobby','age':21}
# db.users.insert_one(doc)
#
# # 한 개 찾기 - 예시
# user = db.users.find_one({'name':'bobby'})
#
# # 여러개 찾기 - 예시 ( _id 값은 제외하고 출력)
# same_ages = list(db.users.find({'age':21},{'_id':False}))
#
# # 바꾸기 - 예시
# db.users.update_one({'name':'bobby'},{'$set':{'age':19}})
#
# # 지우기 - 예시
# db.users.delete_one({'name':'bobby'})