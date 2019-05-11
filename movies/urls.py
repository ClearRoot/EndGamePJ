from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('list', views.list, name='list'),
    path('<int:movie_id>', views.detail, name='detail'),
    path('<int:movie_id>/comment', views.comment_create, name='comment_create'),
    path('<int:movie_id>/<int:comment_id>/update', views.comment_update, name='comment_update'),
    path('<int:movie_id>/<int:comment_id>/delete', views.comment_delete, name='comment_delete'),
    
    path('crawling', views.crawling, name='crawling'),
    path('<int:movie_id>/update', views.update, name='update'),
    path('<int:movie_id>/delete', views.delete, name='delete'),
]