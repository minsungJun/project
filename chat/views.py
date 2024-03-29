# Create your views here.
# chat/views.py
from django.shortcuts import render, redirect
#from django.utils import timezone
from .models import GameRoom, GameAttend, GameWatch
from django.core.paginator import Paginator
from .forms import RoomForm
from django.contrib.auth.models import User
from rank.models import UserRank

#추가사항
#대기실에 관전자 입장 함수


#메인화면
def index(request):
    '''메인 화면'''
    '''Game_room 목록 출력'''

    #메인 화면 접속 시에 사용자가 특정 게임 룸에 입장 상태라면 강제퇴장 처리
    if request.user.is_authenticated == True:
        player = User.objects.get(username = request.user.username)
        if GameAttend.objects.filter(user = player).exists() == True:
            game_room = GameAttend.objects.get(user = player).gameroom
            return redirect('chat:exit_room', room_name=game_room.room_url)

    #입력 인자, GET방식 요청 url에서 page값을 가져올때 사용(즉, 최초 페이지를 물러올때 보여줄 페이지를 설정하는 것)
    page = request.GET.get('page', '1') #페이지
    kw = request.GET.get('kw', '')  # 검색어

    #조회
    game_room_list = GameRoom.objects.order_by('is_start', '-id') #and GameRoom.objects.order_by('-id')

    if kw:
        game_room_list = (
            game_room_list.filter(room_name__icontains=kw) | 
            game_room_list.filter(host__icontains=kw) 
        ).distinct()
    
    #페이징 처리, 페이징 구현에 사용되는 실질적인 클래스(Paginator클래스)
    paginator = Paginator(game_room_list, 20) # 페이지당 10개씩 보여 주기, question_list를 페이지 객체 paginator로 변환
    page_obj = paginator.get_page(page) # 페이징 구현에 사용한 Paginator클래스, 기본적으로 다양한 속성을 가짐 P.133
    print('여기는 실행?')

    context = {'game_room_list': page_obj, 'page': page, 'kw': kw}
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
        player = User.objects.get(username= request.user.username) #현제 로그인 중인 유저의 db
        #is_valid()는 폼값이 유효한지 검사, 현제 로그인중인 유저가 게임 참가중db에 이름이 없으면
        #게임룸을 제작
        if form.is_valid() and not GameAttend.objects.filter(user=player).exists():
            #form으로 Gmae_room모델의 데이터를 저장
            #commit=False는 임시저장을 의미
            game_room = form.save(commit=False)
            game_room.host = request.user.username
            game_room.people_num = game_room.people_num+1
            game_room.save()
            GameAttend(gameroom=game_room, user=player).save()
            #chat라는 앱의 room이라는 이름의 url실행
            return redirect('chat:waiting_room', room_name = game_room.room_url) #방생성시 db에 저장하고 대기실로 입장
        #방 생성시 form이 유효하지만 참가자 db에 유저가 존재할시 참가중인 방으로 이동하도록 make_room호출
        else: #if form.is_valid() and GameAttend.objects.filter(user=player).exists():
            print(request.method)
            print(request.POST)
            game_room = GameAttend.objects.get(user=player).gameroom
            game_room_name = game_room.room_name
            game_room_url = game_room.room_url
            #is_error = "true"
            user_name = player.username

            return render(request, 'chat/make_room.html', {
                "game_room" : game_room,
                "user" : player,
                "is_error" : True,
            })
            #print('현재 다름 게임룸에 참가중')#이를 오류페이지로 만들어서 제공
            #return render(request, 'chat/1.html')
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
    
    game_room = GameRoom.objects.get(room_url = room_name) #입장할 게임룸의 db
    player = User.objects.get(username= request.user.username) #입장하는 유저의db

    print(game_room.people_num)
    #게임의 플레이어로 GameAttend에 저장하고
    #대기실에 들어가도록 한다.
    #유저의 이름이 GameAttend에 저장되어 있지 않고 참가자의 수가 2미만이면 db생성
    #게임 참가자가 아나면서 참가자 수가 2미만이면 게임참가 db에 이름 저장
    if game_room.people_num < 2 and not GameAttend.objects.filter(user=player).exists():
        game_attend = GameAttend(gameroom=game_room, user=player)
        game_attend.save()
        game_room.people_num += 1
        game_room.save()
    #게임 참가자db에 게임 참가자가 2이상이고 로그인 유저가 참가자 db에 이름이 없으면 관전자로 빼냄
    #일단 관전자 제외
    """elif game_room.people_num >= 2 and not GameAttend.objects.filter(user=player).exists():
        game_watch = GameWatch(gameroom=game_room, user=player)
        game_watch.save()"""
    
    game_attend = GameAttend.objects.filter(gameroom=game_room) #게임 룸에 참자 중인 모든 참가자 객체 추출
    print(game_attend)
    attender_count = game_attend.count() #게임 참가자 수
    ready_count = 0
    if game_attend.count() == 2: #참가자의 수가 2이라면
        for attender in game_attend:
            if attender.user_ready == True:
                ready_count = ready_count + 1 #참가자들 중에서 ready중인 참가자 수를 셈
        
    #대기실 입장
    return render(request, 'chat/waiting_room.html', {
        'room_name': room_name, #방 url넘버라서 필요
        'user_name': request.user.username, #방안에서 채팅 구현하여서 필요
        'user': player,
        'attender_count': attender_count,
        'ready_count': ready_count,
        'game_room': game_room, #게임룸 db
        'game_attend': game_attend #게임 참가자 중인 모든 참가자 db
    })

def exit_room(request, room_name):
    '''게임룸 퇴장'''

    if request.user.is_authenticated == False:
        return redirect('common:login')
    
    game_room = GameRoom.objects.get(room_url = room_name) #입장할 게임룸의 db
    player = User.objects.get(username= request.user.username) #입장하는 유저의 db
    game_attend = GameAttend.objects.get(user=player) #유저가 참가중인 게임룸의 db
    
    print(request.method)
    
    game_attend.delete()
    game_room.people_num = game_room.people_num - 1
    game_room.save()
    if game_room.people_num == 0:
        game_room.delete()

    return redirect('chat:index')

def game_ready(request, room_name):
    '''게임 준비 처리'''

    if request.user.is_authenticated == False:
        return redirect('common:login')
    
    player = User.objects.get(username= request.user.username) #입장하는 유저의 db
    #game_attend = GameAttend.objects.get(user=player) #유저가 참가중인 게임룸의 db
    #레디 여부는 게임 참가자 db에 저장

    if player.users.user_ready == False:
        player.users.user_ready = True
        player.users.save()
    else:
        player.users.user_ready = False
        player.users.save()
    
    #return redirect('chat:waiting_room', room_name)
    return redirect('chat:waiting_room', room_name)

def game_start(request, room_name):
    '''게임 시작'''

    if request.user.is_authenticated == False:
        return redirect('common:login')
    
    ready_count = 0
    
    game_room = GameRoom.objects.get(room_url = room_name) #입장할 게임룸의 db
    game_attend = GameAttend.objects.filter(gameroom=game_room)
    
    if game_attend.count() == 2:
        for attender in game_attend:
            if attender.user_ready == True:
                ready_count = ready_count + 1
    
    if game_attend.count() == 2 and ready_count == 2:
        game_room.is_start = True
        game_room.save()
        return redirect('chat:room', room_name)
    else:
        return redirect('chat:waiting_room', room_name)


def game_over(request, room_name):
    if request.user.is_authenticated == False:
        return redirect('common:login')#로그인 여부
    
    player = User.objects.get(username= request.user.username)#플레이어DB
    game_attend = GameAttend.objects.get(user=player)#참가중인 방 DB
    player_rank = UserRank.objects.get(user=player)#유저 랭킹

    #POST로 데이터 입력시 랭킹 처리
    if request.method == "POST":
        
        player_rank.total_game += 1

        if request.POST['is_win_input'] == '0': #win
            player_rank.win_game += 1
            player_rank.rating += 15
            player_rank.is_winning_streak += 1
            if player_rank.is_winning_streak > player_rank.top_winning_streak:
                player_rank.top_winning_streak = player_rank.is_winning_streak

        elif request.POST['is_win_input'] == '1': #lose
            player_rank.lose_game += 1
            player_rank.rating -= 7
            player_rank.is_winning_streak = 0

        else: #3 = draw
            player_rank.rating +=3

        #최고점수 갱신
        if int(request.POST["score_input"]) > player_rank.top_score:
            player_rank.top_score = int(request.POST["score_input"])
            player_rank.rating += 10
        
        player_rank.save()

    game_attend.user_ready = False
    game_attend.save()

    game_attend.gameroom.is_start = False
    game_attend.gameroom.save()

    return redirect("chat:waiting_room", room_name)