from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#게임,채팅 룸 DB
class GameRoom(models.Model):
    room_name = models.CharField(max_length=50)
    room_url = models.CharField(max_length=50)
    #외래키 사용? 굳이? 방장 권한의 경우 html에서 로그인 한사람 id받아와서 form에 저장후 이후부터 host값과 조작자가 같은지 비교하면 가능
    #만약 방장이 나간다면 host를 바꿀수 있나?(외래키를 쓰지 않을 경우에, 외래키는 null값으로 바꾸든 다른 함수를 실행 시키든 가능할지도?)
    #host = models.ForeignKey(User, on_delete=models.SET_NULL)
    host = models.CharField(max_length=50)
    people_num = models.IntegerField(default=0) #player_num
    #people_watch_num = models.IntegerField(default=0) #관전자수

    def __str__(self) -> str:
        return self.room_name

class GameAttend(models.Model):
    gameroom = models.ForeignKey(
        GameRoom,
        on_delete=models.CASCADE,
        related_name='gamerooms', #참조시 gameattend_set대신에 사용, 역참조시에도 사용
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='users'
    )
    
    def __str__(self) -> str:
        return f'{self.gameroom}: {self.user}'

class GameWatch(models.Model):
    gameroom = models.ForeignKey(
        GameRoom,
        on_delete=models.CASCADE,
        related_name='gameroom_watch',
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_watch',
    )

    def __str__(self) -> str:
        return f'{self.gameroom}: {self.user}'