from django.shortcuts import get_object_or_404
from .models import Genre, Movie, People, MovieVideo, RecommendMovie, SimilarMovie
from bs4 import BeautifulSoup
import requests
import datetime
import os

def themovie():
    """json"""
    # JSON_URL = f'https://api.themoviedb.org/3/movie/{movie_key}?api_key={API_KEY}&callback=json&language={language_list[0]}'
    language_list = ['ko-KR', 'en-US'] #0:한국어, 1:영어
    size_list = ['original', 'w500']
    API_KEY = os.getenv('API_KEY')
    URL = 'https://api.themoviedb.org/3/'
    movie_code = []
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
                movie_code.append(movie_key)
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
                #     videos_results = videos_json.get('results')
                #     if videos_results and len(videos_results):
                #         for v in range(len(videos_results)):
                #             key = videos_results[v].get('key')
                #             name = videos_results[v].get('name')
                #             site = videos_results[v].get('site')
                #             size = videos_results[v].get('size')
                #             vtype = videos_results[v].get('type')
                #             MovieVideo.objects.get_or_create(movie=movie[0], key=key, name=name, site=site, size=size, vtype=vtype)
                
                """credits_url"""
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
                        
    print("영화 완료!")
    
    movies = Movie.objects.all()
    for m in movies:
        """recommend_url"""
        for p in range(2):#40개만 추천
            recommend_url = f'{URL}movie/{m.id}/recommendations?api_key={API_KEY}&language={language_list[0]}&page={p}'
            recommend_res = requests.get(recommend_url)
            if recommend_res.status_code == 200:
                recommend_json = recommend_res.json()
                recom_results = recommend_json.get('results')
                for r in range(len(recom_results)):
                    recom_key = recom_results[r].get('id')
                    try:
                        recom_movie = Movie.objects.get(pk=recom_key)
                    except Movie.DoesNotExist:
                        recom_movie = None
                    if recom_movie:
                        code = recom_key
                        recommend_movie = RecommendMovie.objects.get_or_create(code=code)
                        recommend_movie[0].movie = m
                        recommend_movie[0].save()
        
        """similar_url"""
        for p in range(2):#40개
            similar_url = f'{URL}movie/{m.id}/similar?api_key={API_KEY}&language={language_list[0]}&page={p}'
            similar_res = requests.get(similar_url)
            if similar_res.status_code == 200:
                similar_json = similar_res.json()
                similar_results = similar_json.get('results')
                for r in range(len(similar_results)):
                    similar_key = similar_results[r].get('id')
                    try:
                        sim_movie = Movie.objects.get(pk=similar_key)
                    except Movie.DoesNotExist:
                        sim_movie = None
                    if sim_movie:
                        code = similar_key
                        similar_movie = SimilarMovie.objects.get_or_create(code=code)
                        similar_movie[0].movie = m
                        similar_movie[0].save()
    print("추천정보 완료!!!")
    # #영화추천
    # #아래 두개는 page가 존재하니 조심
    # recommend_url = f'{URL}movie/{movie_key}/recommendations?api_key={API_KEY}&language={language_list[0]}&page={page}'
    # similar_url = f'{URL}movie/{movie_key}/similar?api_key={API_KEY}&language={language_list[0]}&page={page}'