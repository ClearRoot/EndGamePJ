from django.shortcuts import get_object_or_404
from .models import Genre, Movie, MovieRank, People, MovieVideo
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
    
    for d in range(1,3):#132,0,-1-20190514
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
            
def themovie():
    """json"""
    # JSON_URL = f'https://api.themoviedb.org/3/movie/{movie_key}?api_key={API_KEY}&callback=json&language={language_list[0]}'
    language_list = ['ko-KR', 'en-US'] #0:한국어, 1:영어
    size_list = ['original', 'w500']
    API_KEY = os.getenv('API_KEY')
    URL = 'https://api.themoviedb.org/3/'
    
    """GENRE"""
    genre_url = f'{URL}genre/movie/list?api_key={API_KEY}&language={language_list[0]}'
    genre_res = requests.get(genre_url)
    if genre_res.status_code == 200:
        genre_json = genre_res.json()
        genres = genre_json.get('genres')
        genres_len = len(genres)
        for i in range(len(genres)):
            genre_id = genres[i].get('id')
            mtype = genres[i].get('name')
            Genre.objects.get_or_create(id=genre_id, mtype=mtype)
    
    print("장르 완성")
    
    # total_page = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=ko-KR&sort_by=popularity.desc'
    """MOVIE"""
    POSTER_URL = f'https://image.tmdb.org/t/p/'
    for page in range(1,11):#page는 1부터 시작함
        discover_url = f'{URL}discover/movie?api_key={API_KEY}&language={language_list[0]}&sort_by=popularity.desc&page={page}'
        discover_res = requests.get(discover_url)
        if discover_res.status_code == 200:
            discover_json = discover_res.json()
            results = discover_json.get('results')
            
            for i in range(len(results)): #len(results)
                movie_key = results[i].get('id')
                print(movie_key)
                title = results[i].get('title')
                poster_path = results[i].get('poster_path')
                image = f'{POSTER_URL}{size_list[1]}{poster_path}'
                backdrop_path = results[i].get('backdrop_path')
                back_image = f'{POSTER_URL}{size_list[0]}{backdrop_path}'
                content = results[i].get('overview')
                release_date = results[i].get('release_date')
                if release_date:
                    open_date = release_date[0:4]
                else:
                    open_date = ""
                genre_ids = results[i].get('genre_ids')
                
                movie = Movie.objects.get_or_create(id=movie_key, title=title, content=content, image=image, back_image=back_image, open_date=open_date)
                print(movie[0])
                if movie[1]:
                    for j in range(len(genre_ids)):
                        genre = get_object_or_404(Genre, id=genre_ids[j])
                        movie[0].genre.add(genre)
                
                # """videos_url"""
                # videos_url = f'{URL}movie/{movie_key}/videos?api_key={API_KEY}&language={language_list[0]}'
                # videos_res = requests.get(videos_url)
                # if videos_res.status_code == 200:
                #     videos_json = videos_res.json()
                #     results = videos_json.get('results')
                #     if len(results):
                #         for v in range(len(results)):
                #             key = results[v].get('key')
                #             name = results[v].get('name')
                #             site = results[v].get('site')
                #             size = results[v].get('size')
                #             vtype = results[v].get('type')
                #             MovieVideo.objects.get_or_create(movie=movie[0], key=key, name=name, site=site, size=size, vtype=vtype)
                # # else: #우리나라 언어가 아닐 때는 보여주지 않는 것으로.
                # #     videos_url = f'{URL}movie/550/videos?api_key={API_KEY}&language={language_list[1]}'
                # #     videos_res = requests.get(videos_url)
                # #     if videos_res.status_code == 200:
                # #         videos_json = videos_res.json()
                # #         results = videos_json.get('results')
                # #         if len(results):
                # #             pass
                
    #             """credits_url"""
                credits_url = f'{URL}movie/{movie_key}/credits?api_key={API_KEY}&language={language_list[0]}'
                credits_res = requests.get(credits_url)
                if credits_res.status_code == 200:
                    credits_json = credits_res.json()
                    cast = credits_json.get('cast')
                    cast_len = len(cast) if len(cast) < 10 else 10
                    for c in range(cast_len):
                        people_key = cast[c].get('id')
                        actor = cast[c].get('name')
                        profile_path = cast[c].get('profile_path')
                        image = f'{POSTER_URL}{size_list[1]}{profile_path}'
                        people = People.objects.get_or_create(people_key=people_key, actor=actor)
                        if people[1]:
                            people[0].image = image
                            people[0].save()
                        people[0].movie.add(movie[0])
                        
                    crew = credits_json.get('crew')
                    for c in range(len(crew)):
                        if str(crew[c].get('job')) == 'Director':
                            people_key = crew[c].get('id')
                            director = crew[c].get('name')
                            profile_path = crew[c].get('profile_path')
                            image = f'{POSTER_URL}{size_list[1]}{profile_path}'
                            people = People.objects.get_or_create(people_key=people_key, director=director)
                            if people[1]:
                                people[0].image = image
                                people[0].save()
                            people[0].movie.add(movie[0])
                        if c > 15:#15안에는 있겠지라는 마음
                            break
    print("모두 완료!")
    
    # #영화추천
    # #아래 두개는 page가 존재하니 조심
    # recommend_url = f'{URL}movie/{movie_key}/recommendations?api_key={API_KEY}&language={language_list[0]}&page={page}'
    # similar_url = f'{URL}movie/{movie_key}/similar?api_key={API_KEY}&language={language_list[0]}&page={page}'