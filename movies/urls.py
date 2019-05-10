from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('list', views.list, name='list'),
    path('<int:movie_id>', views.detail, name='detail'),
    
    path('crawling', views.crawling, name='crawling'),
    path('<int:movie_id>/update', views.update, name='movie_admin_update'),
    path('<int:movie_id>/delete', views.delete, name='movie_admin_delete'),
]