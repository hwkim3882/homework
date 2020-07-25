
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

target_movie = db.movies.find_one({'title':'월-E'})
target_star = target_movie['star']
print(target_star)

db.movies.update_many({'star':target_star},{'$set':{'star':'0'}})