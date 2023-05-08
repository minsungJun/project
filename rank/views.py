from django.shortcuts import render, redirect
from .models import UserRank
from django.core.paginator import Paginator

# Create your views here.

#랭킹 화면
def index(request):
    #입력 인자, GET방식 요청 url에서 page값을 가져올때 사용(즉, 최초 페이지를 물러올때 보여줄 페이지를 설정하는 것)
    page = request.GET.get('page', '1') #페이지

    #조회
    game_room_list = UserRank.objects.order_by('-id')

    #페이징 처리, 페이징 구현에 사용되는 실질적인 클래스(Paginator클래스)
    paginator = Paginator(game_room_list, 10) # 페이지당 10개씩 보여 주기, question_list를 페이지 객체 paginator로 변환
    page_obj = paginator.get_page(page) # 페이징 구현에 사용한 Paginator클래스, 기본적으로 다양한 속성을 가짐 P.133

    context = {'game_room_list': page_obj}
    return render(request, 'chat/index.html', context)