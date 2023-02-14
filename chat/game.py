from .models import GameRoom, GameAttend, GameWatch
from .forms import RoomForm
from django.contrib.auth.models import User


def test(input_url, input_name):
    temp = GameRoom.objects.get(room_url=input_url)
    if temp.turn % 2 == 0:
        if temp.host == input_name:
            return True
        else:
            return False
    elif temp.turn % 2 == 1:
        if temp.guest == input_name:
            return True
        else:
            return False
    