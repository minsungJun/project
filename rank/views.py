from django.shortcuts import render, redirect
from .models import UserRank
from django.core.paginator import Paginator
from django.db.models import F, FloatField, ExpressionWrapper
from django.contrib.auth.models import User

# Create your views here.

#랭킹 화면
def index(request):
    #입력 인자, GET방식 요청 url에서 page값을 가져올때 사용(즉, 최초 페이지를 물러올때 보여줄 페이지를 설정하는 것)
    page = request.GET.get('page', '1') #페이지
    kw = request.GET.get('kw', '')  # 검색어

    #조회
    user_rank_list = UserRank.objects.order_by('-total_game')
    if kw:
        player = User.objects.get(username=kw)
        for user_rank, i in zip(user_rank_list,range(user_rank_list.count())):
            if user_rank.user == player:
                rank_num = i+1
        user_rank_list = user_rank_list.filter(user=player)
        paginator = Paginator(user_rank_list, 20)
        page_obj = paginator.get_page(page)
        return render(request, 'rank/rank.html', {
            'user_rank_list': page_obj,
            'rank_num': rank_num,
            'is_search': True,
        })

    #페이징 처리, 페이징 구현에 사용되는 실질적인 클래스(Paginator클래스)
    paginator = Paginator(user_rank_list, 20) # 페이지당 10개씩 보여 주기, question_list를 페이지 객체 paginator로 변환
    page_obj = paginator.get_page(page) # 페이징 구현에 사용한 Paginator클래스, 기본적으로 다양한 속성을 가짐 P.133

    context = {'user_rank_list': page_obj}
    return render(request, 'rank/rank.html', context)

def total_game(request):
    page = request.GET.get('page', '1') #페이지

    #조회
    user_rank_list = UserRank.objects.order_by('-total_game')

    paginator = Paginator(user_rank_list, 20) 
    page_obj = paginator.get_page(page) 

    context = {'user_rank_list': page_obj}
    return render(request, 'rank/rank.html', context)

def win_game(request):
    page = request.GET.get('page', '1') #페이지

    #조회
    user_rank_list = UserRank.objects.order_by('-win_game')

    paginator = Paginator(user_rank_list, 20) 
    page_obj = paginator.get_page(page) 

    context = {'user_rank_list': page_obj}
    return render(request, 'rank/rank.html', context)

def win_rate(request):
    page = request.GET.get('page', '1') #페이지

    #임의의 속성을 만들어 조회
    user_rank_list = UserRank.objects.annotate(
    win_rate=ExpressionWrapper(
        F('win_game') / F('total_game')*100, 
        output_field=FloatField()
    )
    ).order_by('win_rate')

    paginator = Paginator(user_rank_list, 20) 
    page_obj = paginator.get_page(page) 

    context = {'user_rank_list': page_obj}
    return render(request, 'rank/rank.html', context)

def rating(request):
    page = request.GET.get('page', '1') #페이지

    #조회
    user_rank_list = UserRank.objects.order_by('-rating')

    paginator = Paginator(user_rank_list, 20) 
    page_obj = paginator.get_page(page) 

    context = {'user_rank_list': page_obj}
    return render(request, 'rank/rank.html', context)

def top_score(request):
    page = request.GET.get('page', '1') #페이지

    #조회
    user_rank_list = UserRank.objects.order_by('-top_score')

    paginator = Paginator(user_rank_list, 20) 
    page_obj = paginator.get_page(page) 

    context = {'user_rank_list': page_obj}
    return render(request, 'rank/rank.html', context)

def user_status(request, user):
    player = User.objects.get(username = user)

    kw = request.GET.get('kw', '')  # 검색어
    if kw:
        player = User.objects.get(username = kw)
        return redirect('rank:user_status', user=player)

    return render(request, 'rank/user_status.html', {
        'user' : player
    })