from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('list', views.list, name='list'),
    path('<int:movie_id>', views.detail, name='detail'),
    path('<int:movie_id>/comment', views.comment_create, name='comment_create'),
    path('<int:movie_id>/<int:comment_id>/comment_update', views.comment_update, name='comment_update'),
    path('<int:movie_id>/<int:comment_id>/comment_delete', views.comment_delete, name='comment_delete'),
    path('<int:movie_id>/score', views.score_create, name='score_create'),
    # path('<int:movie_id>/<int:score_id>/score_update', views.score_update, name='score_update'),
    path('<int:movie_id>/<int:score_id>/score_delete', views.score_delete, name='score_delete'),
    
    path('json/list', views.json_list, name='json_list'),
    path('json/<int:movie_id>', views.json_detail, name='json_detail'),
    path('json/<int:movie_id>/comment', views.json_comment, name='json_comment'),
    
    path('crawling', views.crawling, name='crawling'),
    path('<int:movie_id>/update', views.update, name='update'),
    path('<int:movie_id>/delete', views.delete, name='delete'),
]