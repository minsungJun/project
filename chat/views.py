# Create your views here.
# chat/views.py
from django.shortcuts import render
from django.utils import timezone


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    if request.user.is_authenticated:  # 만약 요청시 로그인 상태라면
        # 채팅방에 들어가도록 한다.
        print("User is logged in :)")
        print(request.user.username)  # 현재 로그인 중인 유저
        # presentTime = timezone.now()

        # 채팅방 입장
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'user_name': request.user.username,

            # 'present_time': presentTime
        })
    else:
        # 비로그인시 로그인 오류를 내보내든가 로그인 창으로 보낸다.
        print("User is not logged in :(")

        # 로그인 창으로 이동
        return render(request, 'common/login.html')