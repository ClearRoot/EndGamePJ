from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_id>', views.user_page, name='user_page'),
    path('follow/<int:user_id>', views.follow, name='follow'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('leaving_user/<int:user_id>', views.leaving_user, name='leaving_user'),
    path('pickup/<int:movie_id>', views.pickup, name='pickup'),
    path('checking', views.password_enter_form, name='password_enter_form'),
]