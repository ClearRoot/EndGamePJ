from django.shortcuts import render, redirect
import datetime
import requests
import os

# Create your views here.
"""
MOVIE_KEY : 영화진흥위원회 오픈API 발급KEY값
targetDt : 어제날짜(금일날짜에 대한 정보는 다음날 나오기에)
URL : json형태로 제공해주는 URL주소
"""
def list(request):
    ###추후 쓸 내용
    # MOVIE_KEY = os.getenv('MOVIE_KEY')
    # targetDt = datetime.datetime.now() - datetime.timedelta(days=1)
    # targetDt = targetDt.strftime('%Y%m%d')
    # URL = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={MOVIE_KEY}&targetDt={targetDt}'
    # res = requests.get(URL)
    # if res.status_code == 200:
    #     print("접근완료")
    #     #json형태를 dict형태로 변환
    #     res = res.json()
    #     #최대 10개가 있으므로
    #     dailyBoxOfficeList = res.get('boxOfficeResult').get('dailyBoxOfficeList')
    #     """
    #     변수설명 및 API
    #     http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do
    #     """
    #     for num in range(10):
    #         rankOldAndNew = dailyBoxOfficeList[num].get('rankOldAndNew')
    #         movieCd = dailyBoxOfficeList[num].get('movieCd')
    #         movieNm = dailyBoxOfficeList[num].get('movieNm')
    #         openDt = dailyBoxOfficeList[num].get('openDt')
    #         audiCnt = dailyBoxOfficeList[num].get('audiCnt')
    #         audiChange = dailyBoxOfficeList[num].get('audiChange')
    #         audiAcc = dailyBoxOfficeList[num].get('audiAcc')
            
    # else:
    #     print("접근실패")
    return render(request, 'movies/list.html')