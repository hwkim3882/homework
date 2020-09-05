import sys
import requests
from bs4 import BeautifulSoup
from gensim.summarization import summarize
from newspaper import Article
from urllib import parse
from flask import Flask, render_template, jsonify, request, redirect
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

import os

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.myproject  # 'dbsparta'라는 이름의 db를 만듭니다.

# print(f"{sys.argv[1]}에 대하여 검색합니다. 최근 뉴스 10 항목")


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

    ## API 역할을 하는 부분

@app.route('/search', methods=['POST'])
def search() :
    word = request.form['title_give']
    keyword_naver = parse.quote(word)
    URL = f"https://search.naver.com/search.naver?where=news&query={keyword_naver}"

    get_requests = requests.get(URL)
    links = BeautifulSoup(get_requests.text, 'html.parser').select('ul.type01 dt a')
    title_s = []
    summary_s = []
    x = 0

    for link in links:
        try:
            s_link = str(link.get("href"))
            news = Article(s_link, language="ko")
            news.download()
            news.parse()
            # print("\n\n\n\n", "-" * 70)
            # print(f"{news.title} \n\n")
            title_s.append(news.title)
            # print(f"{summarize(news.text, word_count=49)}")
            summary_s.append(summarize(news.text, word_count=49))

            # print(title_s[x], summary_s[x])
            x += 1

        except:
            print("\n\n\n\n", "-" * 70)
            print("undefined")

    doc = {
        'search_word': word,
        'title' : title_s,
        'summary': summary_s

    }
    db.search_result.insert_one(doc)

    return jsonify({'result':'success', 'summary': summary_s, 'title': title_s})

@app.route('/search_list', methods=['POST'])
def search_list():

    title_receive = request.form['title_give']
    print(title_receive)

    # 1. DB에서 리뷰 정보 모두 가져오기
    search_list = list(db.search_result.find({'search_word': title_receive }, {'_id': 0}))
    print(search_list)
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'search_list': search_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)