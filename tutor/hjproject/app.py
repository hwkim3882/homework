from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from datetime import datetime
from flask import request, redirect


app = Flask(__name__)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.myproject  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def upload_tap():
    return render_template('upload_tap.html')

@app.route('/main_page')
def main_page():
    return render_template('main_page.html')
#
@app.route('/dayday')
def dayday():
    return render_template('dayday.html')


## API 역할을 하는 부분
@app.route('/review', methods=['POST'])
def write_review():
    # title_receive로 클라이언트가 준 title 가져오기
    #picture_receive = request.form['picture_give']
    # author_receive로 클라이언트가 준 author 가져오기
    writer_receive = request.form['writer_give']
    # review_receive로 클라이언트가 준 review 가져오기
    review_receive = request.form['review_give']

    datetime.today()
    date_receive = datetime.today().day
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # print(date_receive)
    # DB에 삽입할 review 만들기
    review = {
        #'picture': picture_receive,
        'writer': writer_receive,
        'review': review_receive,
        'date': days[date_receive]
    }
    # reviews에 review 저장하기
    db.myproject.insert_one(review)

    # writer = db.myprojectMission.find_one({'writer': 'sasa'})
    # print(writer)

    writer = db.myprojectMission.find_one({'writer': writer_receive})

    def update_dayday(date):
        if date == 'Monday' :
            db.myprojectMission.update_one({'writer': writer_receive}, {'$set': {'Monday': 'o'}})
        elif date == 'Tuesday' :
            db.myprojectMission.update_one({'writer': writer_receive}, {'$set': {'Tuesday': 'o'}})
        elif date == 'Wednesday' :
            db.myprojectMission.update_one({'writer': writer_receive}, {'$set': {'Wednesday': 'o'}})
        elif date == 'Thursday' :
            db.myprojectMission.update_one({'writer': writer_receive}, {'$set': {'Thursday': 'o'}})
        elif date == 'Friday' :
            db.myprojectMission.update_one({'writer': writer_receive}, {'$set': {'Friday': 'o'}})
        elif date == 'Saturday' :
            db.myprojectMission.update_one({'writer': writer_receive}, {'$set': {'Saturday': 'o'}})
        elif date == 'Sunday' :
            db.myprojectMission.update_one({'writer': writer_receive}, {'$set': {'Sunday': 'o'}})

    if writer is None:
        review_list = {'writer': writer_receive,
                       "Monday": 'x',
                      "Tuesday" : 'x',
                      "Wednesday" : 'x',
                      "Thursday" : 'x',
                      "Friday" : 'x',
                      "Saturday" : 'x',
                      "Sunday" : 'x'}
        db.myprojectMission.insert_one(review_list)
        print(days[date_receive])
        update_dayday(days[date_receive])

    else:
        update_dayday(days[date_receive])

    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})



@app.route('/review', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.myproject.find({}, {'_id': 0}))
    # 새로운 디비 추가
    reviews_dayday = list(db.myprojectMission.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews, 'reviews_dayday':reviews_dayday})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


