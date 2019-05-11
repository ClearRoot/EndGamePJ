from .models import Genre, Movie, MovieRank, People
from bs4 import BeautifulSoup
import requests
import datetime
import os

def movie_data():
    """슈퍼유저만 데이터 크롤링, 안전성을 위해 주석화"""
    MOVIE_KEY = os.getenv('MOVIE_KEY')
    NAVER_ID = os.getenv('NAVER_ID')
    NAVER_KEY = os.getenv('NAVER_KEY')
    
    genre_list = {
        '드라마':1, '코미디':2, '액션':3, '멜로/로맨스':4, '스릴러':5,
        '미스터리':6, '공포(호러)':7, '어드벤처':8, '범죄':9, '가족':10,
        '판타지':11, 'SF':12, '서부극(웨스턴)':13, '사극':14, '애니메이션':15,
        '다큐멘터리':16, '전쟁':17, '뮤지컬':18, '성인물(에로)':19, '공연':20,
        '기타':21
    }
    
    for d in range(130,0,-1):#130-20190511
        date = datetime.datetime.now() - datetime.timedelta(days=d)
        date = date.strftime('%Y%m%d')
    
        URL = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={MOVIE_KEY}&targetDt={date}'
        res = requests.get(URL)
        if res.status_code == 200:

            res = res.json()
            daily_movies = res.get('boxOfficeResult').get('dailyBoxOfficeList')
            for num in range(10):
                rank = daily_movies[num].get('rank')
                rank_inten = daily_movies[num].get('rankInten')
                movie_code = daily_movies[num].get('movieCd')
                title = daily_movies[num].get('movieNm')
                open_date = daily_movies[num].get('openDt')
                audience = int(daily_movies[num].get('audiAcc'))
                data = requests.get('https://openapi.naver.com/v1/search/movie.json?query='+title,
                    headers = {
                        'X-Naver-Client-Id':NAVER_ID,
                        'X-Naver-Client-Secret':NAVER_KEY
                    }
                )
                data = data.json()
                
                movie_link = data.get('items')[0].get('link')
                movie_link_url = requests.get(movie_link)
                
                
                if movie_link_url.status_code == 200:
                    soup = BeautifulSoup(movie_link_url.text, features='html.parser')
                    content = soup.select('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p')
                    if content:
                        content = str(content[0])
                    else:
                        content = ''
                
                movie_img_code = movie_link.split('https://movie.naver.com/movie/bi/mi/basic.nhn?code=')
                if movie_img_code[1]:
                    print(movie_img_code[1], title)
                    movie_img_url = f'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={movie_img_code[1]}'
                    movie_img_url = requests.get(movie_img_url)
                    if movie_img_url.status_code == 200:
                        soup = BeautifulSoup(movie_img_url.text, features='html.parser')
                        image = soup.select('#targetImage')
                        image = image[0].get('src')
                else:
                    image = 'http://tinamovie.com/wp-content/uploads/2018/10/nopicture.jpg'
    
                detail_url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={MOVIE_KEY}&movieCd={movie_code}'
                detail_res = requests.get(detail_url)
                if detail_res.status_code == 200:
                    detail_res = detail_res.json()
                    movie_info = detail_res.get('movieInfoResult').get('movieInfo')
                    
                    grade = movie_info.get('audits')[0].get('watchGradeNm')
                    nations = movie_info.get('nations')[0].get('nationNm')
                    show_time = int(movie_info.get('showTm'))
                    
                    """ Movie Table """
                    movie = Movie.objects.get_or_create(title=title, content=content, open_date=open_date, image=image, grade=grade, nations=nations, show_time=show_time)
                    movie[0].audience = audience
                    movie[0].save()
                    for i in range(len(movie_info.get('genres'))):
                        idx = genre_list[movie_info.get('genres')[i].get('genreNm')]
                        genre = Genre.objects.get(pk=idx)
                        movie[0].genre.add(genre)
                    
                    if movie[1]:
                        """ People Table """                
                        for director in range(len(movie_info.get('directors'))):
                            people = People.objects.get_or_create(director=movie_info.get('directors')[director].get('peopleNm'))
                            people[0].movie.add(movie[0])
                        
                        for actor in range(len(movie_info.get('actors'))):
                            people = People.objects.get_or_create(actor=movie_info.get('actors')[actor].get('peopleNm'))
                            people[0].movie.add(movie[0])
                    
                    """ MovieRank Table """
                    MovieRank.objects.get_or_create(movie=movie[0], date=date, rank=rank, rank_inten=rank_inten)
                    
                    print(f'{date}, {num}번째 완료!!!!!')
            
        else:
            print("접근실패")