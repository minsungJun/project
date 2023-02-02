from django.urls import path

from . import views

app_name = 'chat'


urlpatterns = [
    path('', views.index, name='index'),
    path('make_room/', views.make_room, name='make_room'),
    path('<str:room_name>/', views.room, name='room'),
    path('waiting_room/<str:room_name>/', views.waiting_room, name='waiting_room'),
]