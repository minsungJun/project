from django.urls import re_path

from . import consumers, consumers2

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/waiting_room/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]