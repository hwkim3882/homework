import requests
from bs4 import BeautifulSoup

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 공통으로 쓰는 URL
musicURL = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713'

# copy-selector에서 tag정보를 일어오기
# rank
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
# 노래 이름
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
# 가수 이름
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis


# 주소를 보면 pg=1,2,3,4로 parameter의 값이 변경되므로, params를 range(1,5)로 주고 4번 반복하기

for page in range(1,5):
    # params 선언, key:value형식
    params = {'pg': page}
    # requests.get에서 params를 추가
    data = requests.get(musicURL, params=params, headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    # param에 따라 가져오는 html이 다르므로 반복해서 새로 가져온다.
    soup = BeautifulSoup(data.text, 'html.parser')
    songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

    for song in songs:
        # td tag안의 하위 태그들의 내용을 가져오지 않으려고 .contents[]를 사용, 빈칸을 지워주려고 strip()사용
        rank = song.select_one('td.number').contents[0].strip()

        singer = song.select_one('td.info>a.artist.ellipsis').text
        #print(rank, singer)
        title = song.select_one('td.info > a.title.ellipsis').text.strip()

        icon_tag = song.select_one('span.icon')
        if icon_tag is not None:
            title = song.select_one('td.info > a.title.ellipsis').contents[1].text
            icon_tag.decompose()
            title += song.select_one('td.info > a.title.ellipsis').text.strip()

        #singer = singer.text.strip()
        print(rank, title, singer)

