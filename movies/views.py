from django.shortcuts import render, redirect
import datetime
import requests
# from bs4 import BeautifulSoup
import os

# Create your views here.
def list(request):
    
    # MOVIE_KEY = os.getenv('MOVIE_KEY')
    # NAVER_ID = os.getenv('NAVER_ID')
    # NAVER_KEY = os.getenv('NAVER_KEY')
    
    # genre_list = ['드라마', '코미디', '액션', '멜로/로맨스', '스릴러',
    #             '미스터리', '공포(호러)', '어드벤처', '범죄', '가족',
    #             '판타지', 'SF', '서부극(웨스턴)', '사극', '애니메이션',
    #             '다큐멘터리', '전쟁', '뮤지컬', '성인물(에로)', '공연',
    #             '기타']
    
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
    #         rank = dailyBoxOfficeList[num].get('rank')
    #         rankInten = dailyBoxOfficeList[num].get('rankInten')
    #         movieCd = dailyBoxOfficeList[num].get('movieCd')
    #         movieNm = dailyBoxOfficeList[num].get('movieNm')
    #         openDt = dailyBoxOfficeList[num].get('openDt')
    #         audiAcc = dailyBoxOfficeList[num].get('audiAcc')
        
    #         data = requests.get('https://openapi.naver.com/v1/search/movie.json?query='+movieNm,
    #             headers = {
    #                 'X-Naver-Client-Id':NAVER_ID,
    #                 'X-Naver-Client-Secret':NAVER_KEY
    #             }
    #         )
    #         data = data.json()
            
    #         movieLink = data.get('items')[0].get('link')
    #         movieLinkURL = requests.get(movieLink)
    #         if movieLinkURL.status_code == 200:
    #             soup = BeautifulSoup(movieLinkURL.text, features='html.parser')
    #             movieContent = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')
    #             movieContent = movieContent[0]
                
    #         movieImgCode = movieLink.split('https://movie.naver.com/movie/bi/mi/basic.nhn?code=')
    #         movieImgURL = f'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={movieImgCode[1]}'
    #         movieImgURL = requests.get(movieImgURL)
    #         if movieImgURL.status_code == 200:
    #             soup = BeautifulSoup(movieImgURL.text, features='html.parser')
    #             movieImg = soup.select('#targetImage')
    #             movieImg = movieImg[0].get('src')

    #         detailURL = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={MOVIE_KEY}&movieCd={movieCd}'
    #         detail_res = requests.get(detailURL)
    #         if detail_res.status_code == 200:
    #             detail_res = detail_res.json()
    #             movieInfo = detail_res.get('movieInfoResult').get('movieInfo')
                
    #             for actor in range(len(movieInfo.get('actors'))):
    #                 ###변경해야함
    #                 actors.append(movieInfo.get('actors')[actor].get('peopleNm'))
                
    #             watchGradeNm = movieInfo.get('audits')[0].get('watchGradeNm')
                
    #             for director in range(len(movieInfo.get('directors'))):
    #                 ###변경해야함
    #                 directors.append(movieInfo.get('directors')[director].get('peopleNm'))
                
    #             for genre in range(len(movieInfo.get('genres'))):
    #                 for idx in range(len(genre_list)):
    #                     pass
                
    #             movieNmEn = movieInfo.get('movieNmEn')
                
    #             nations = movieInfo.get('nations')[0].get('nationNm')
                
    #             showTm = movieInfo.get('showTm')
    #             print(f'{num}번째 완료!!!!!')
        
    # else:
    #     print("접근실패")
    
    return render(request, 'movies/list.html')