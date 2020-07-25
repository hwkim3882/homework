from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 설치 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는# 이름의 db를 만듭니다.

all_users = db.users.find_one({'age':40}, {'_id':False})

db.users.update_one({'name': '덤블도어'}, {'$set': {'age': 19}})

db.users.delete_one({'name':'론'})