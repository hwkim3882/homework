import requests
from bs4 import BeautifulSoup

import openpyxl

# 엑셀 파일 만들기
workbook = openpyxl.Workbook()

# 활성된 시트 불러오기
workbook = openpyxl.Workbook()
sheet = workbook.active

#시트 이름 바꾸기
sheet.title = 'movie'

sheet.cell(row=1, column=1).value = 'ranking'
sheet.cell(row=1, column=2).value = 'title'
sheet.cell(row=1, column=3).value = 'star'

print(sheet.cell(row=1,column=1).value)


# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
movies = soup.select('#old_content > table > tbody > tr')

# movies (tr들) 의 반복문을 돌리기
rank = 1
row = 2
for movie in movies:
    # movie 안에 a 가 있으면,≠
    a_tag = movie.select_one('td.title > div > a')
    if a_tag is not None:
        title = a_tag.text
        star = movie.select_one('td.point').text
        #print(rank, title, star)

        # 시트에 값 넣어주기
        sheet.cell(row = row, column = 1, value = rank)
        sheet.cell(row = row, column = 2, value = title)
        sheet.cell(row = row, column = 3, value = star)

        rank += 1
        row += 1

workbook.save('movieranking.xlsx')
