from django.urls import path

from . import views

app_name = 'rank'

urlpatterns = [
    path('', views.index, name='index'),
    path('total_game/', views.total_game, name='total_game'),
    path('win_game/', views.win_game, name='win_game'),
    path('win_rate/', views.win_rate, name='win_rate'),
    path('rating/', views.rating, name='rating'),
    path('top_score/', views.top_score, name='top_score'),
]