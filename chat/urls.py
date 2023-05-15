from django.urls import path

from . import views

app_name = 'chat'


urlpatterns = [
    path('', views.index, name='index'),
    path('make_room/', views.make_room, name='make_room'),
    path('<str:room_name>/', views.room, name='room'),
    path('waiting_room/<str:room_name>/', views.waiting_room, name='waiting_room'),
    path('<str:room_name>/exit/', views.exit_room, name='exit_room'),
    path('<str:room_name>/ready/', views.game_ready, name='game_ready'),
    path('<str:room_name>/start/', views.game_start, name='game_start'),
    path('<str:room_name>/game_over/', views.game_over, name='game_over'),
]