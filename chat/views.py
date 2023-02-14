# Create your views here.
# chat/views.py
from django.shortcuts import render, redirect
#from django.utils import timezone
from .models import GameRoom, GameAttend, GameWatch
from django.core.paginator import Paginator
from .forms import RoomForm
from django.contrib.auth.models import User

#추가사항
#대기실에 관전자 입장 함수


#메인화면
def index(request):
    '''Game_room 목록 출력'''

    #입력 인자, GET방식 요청 url에서 page값을 가져올때 사용(즉, 최초 페이지를 물러올때 보여줄 페이지를 설정하는 것)
    page = request.GET.get('page', '1') #페이지

    #조회
    game_room_list = GameRoom.objects.order_by('-id')

    #페이징 처리, 페이징 구현에 사용되는 실질적인 클래스(Paginator클래스)
    paginator = Paginator(game_room_list, 10) # 페이지당 10개씩 보여 주기, question_list를 페이지 객체 paginator로 변환
    page_obj = paginator.get_page(page) # 페이징 구현에 사용한 Paginator클래스, 기본적으로 다양한 속성을 가짐 P.133

    context = {'game_room_list': page_obj}
    return render(request, 'chat/index.html', context)


#게임룸 만들기
def make_room(request):
    #로그인 여부 확인
    if request.user.is_authenticated == False:
        return redirect('common:login')

    if request.method == 'POST':
        #화면에서 받은 데이터로 폼값을 채움
        form = RoomForm(request.POST) 
        print(form)
        player = User.objects.get(username= request.user.username) #현제 로그인 중인 유저의 db ##
        #is_valid()는 폼값이 유효한지 검사, 현제 로그인중인 유저가 게임 참가중db에 이름이 없으면 
        #게임룸을 제작
        if form.is_valid() and not GameAttend.objects.filter(user=player).exists(): ##
            #form으로 Gmae_room모델의 데이터를 저장
            #commit=False는 임시저장을 의미
            game_room = form.save(commit=False)
            game_room.host = request.user.username
            game_room.people_num = game_room.people_num+1
            game_room.turn = 0
            game_room.save()
            GameAttend(gameroom=game_room, user=player).save()
            #chat라는 앱의 room이라는 이름의 url실행
            return redirect('chat:waiting_room', room_name = game_room.room_url) #방생성시 db에 저장하고 대기실로 입장
        else:
            print('현재 다름 게임룸에 참가중')#이를 오류페이지로 만들어서 제공
            return render(request, 'chat/1.html')
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'chat/make_room.html', context)


#게임룸 바로 입장?, 필요? 나중에 삭제?, 무조건 대기실을 거쳐야 하는데 필요?
def room(request, room_name):
    #로그인 여부 확인
    if request.user.is_authenticated == False:
        return redirect('common:login')

    print("User is logged in :)")
    print(request.user.username)  # 현재 로그인 중인 유저
    # presentTime = timezone.now()

    # 채팅방 입장
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user_name': request.user.username,

        # 'present_time': presentTime
    })
    


#대기실 입장
def waiting_room(request, room_name):
    '''대기실 입장 가능여부 확인 및 처리'''
    #로그인 여부 확인
    if request.user.is_authenticated == False:
        return redirect('common:login')
    '''#print(request.POST.get())
    #print(request.GET.get())
    game_room = GameRoom.objects.get(room_url = room_name) #입장할 게임룸의 db
    player = User.objects.get(username= request.user.username) #입장하는 유저의db

    print(request.method)

    #입력방식이 POST라면 메인화면으로
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('exit'))
        print(request.POST.get('exit2'))
        game_attend = GameAttend.objects.get(user=player)
        game_attend.delete()
        game_room.people_num = game_room.people_num - 1
        if game_room.people_num == 0:
            game_room.delete()
        
        #print(request.GET.get())
        if request.POST.get('exit2'):
            return redirect('chat:index')'''
    if request.method == "POST":
        return redirect('chat:exit_room',room_name=room_name)
    
    game_room = GameRoom.objects.get(room_url = room_name) #입장할 게임룸의 db
    player = User.objects.get(username= request.user.username) #입장하는 유저의db

    print(game_room.people_num)
    #게임의 플레이어로 GameAttend에 저장하고
    #대기실에 들어가도록 한다.
    #유저의 이름이 GameAttend에 저장되어 있지 않고 참s가자의 수가 2미만이면 db생성
    #게임 참가자가 아나면서 참가자 수가 2미만이면 게임참가 db에 이름 저장
    if game_room.people_num < 2 and not GameAttend.objects.filter(user=player).exists():
        game_attend = GameAttend(gameroom=game_room, user=player)
        game_attend.save()
        game_room.guest = request.user.username
        game_room.people_num += 1
        game_room.save()
    #게임 참가자db에 게임 참가자가 2이상이고 로그인 유저가 참가자 db에 이름이 없으면 관전자로 빼냄
    elif game_room.people_num >= 2 and not GameAttend.objects.filter(user=player).exists():
        game_watch = GameWatch(gameroom=game_room, user=player)
        game_watch.save()
        
        
    """if (game_room.people_num < 2)and(not(GameAttend.objects.get(user__exist=player))):
            game_attend = GameAttend(gameroom=game_room, user=player)
            game_attend.save()
            game_room.people_num += 1
            game_room.save()"""
    """try:
        if (game_room.people_num < 2)and(not(player.users)):
            game_attend = GameAttend(gameroom=game_room, user=player)
            game_attend.save()
            game_room.people_num += 1
            game_room.save()
    except:
        game_attend = GameAttend(gameroom=game_room, user=player)
        game_attend.save()
        game_room.people_num += 1
        game_room.save()"""
        
        
        
    #대기실 입장
    return render(request, 'chat/waiting_room.html', {
        'room_name': room_name, #방 url넘버라서 필요
        'user_name': request.user.username, #방안에서 채팅 구현하여서 필요
    })

def exit_room(request, room_name):
    '''게임룸 퇴장'''

    if request.user.is_authenticated == False:
        return redirect('common:login')
    
    game_room = GameRoom.objects.get(room_url = room_name)     #입장할 게임룸의 db
    player = User.objects.get(username= request.user.username) #입장하는 유저의 db
    game_attend = GameAttend.objects.get(user=player)          #유저가 참가중인 게임룸의 db
    
    print(request.method)
    
    game_attend.delete()
    game_room.people_num = game_room.people_num - 1
    game_room.save()
    if game_room.people_num == 0:
        game_room.delete()

    return redirect('chat:index')