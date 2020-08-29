import sys
import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize
from newspaper import Article
from urllib import parse
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.myproject  # 'dbsparta'라는 이름의 db를 만듭니다.

# print(f"{sys.argv[1]}에 대하여 검색합니다. 최근 뉴스 10 항목")


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

    ## API 역할을 하는 부분


@app.route('/review', methods=['POST'])
def write_review():
    # title_receive로 클라이언트가 준 title 가져오기
    title_receive = request.form['title_give']

    # DB에 삽입할 review 만들기
    review = {
        'title': title_receive,

    }
    # reviews에 review 저장하기
    db.reviews.insert_one(review)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '검색완료.'})

@app.route('/search', methods=['POST'])
def search() :
    word = request.form['title_give']
    keyword_naver = parse.quote(word)
    URL = f"https://search.naver.com/search.naver?where=news&query={keyword_naver}"

    get_requests = requests.get(URL)
    links = BeautifulSoup(get_requests.text, 'html.parser').select('ul.type01 dt a')

    for link in links:
        try:
            s_link = str(link.get("href"))
            news = Article(s_link, language="ko")
            news.download()
            news.parse()
            # print("\n\n\n\n", "-" * 70)
            # print(f"{news.title} \n\n")
            title = news.title
            # print(f"{summarize(news.text, word_count=49)}")
            summary = summarize(news.text, word_count=49)
            print(title, summary)

        except:
            print("\n\n\n\n", "-" * 70)
            print("undefined")
    return



@app.route('/review', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.reviews.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)