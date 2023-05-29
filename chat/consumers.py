from channels.generic.websocket import AsyncWebsocketConsumer
import json
from chat import game_system, game
from channels.db import database_sync_to_async


room = {}
room_turn = {}
user_score = {}


class ChatConsumer(AsyncWebsocketConsumer):

    sys = None


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.sys = game_system.System()
        # "room" 그룹에 가입
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # "room" 그룹에서 탈퇴
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓 으로 부터 메시지 수신
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('웹소켓에서 받은 JSON 형식 : ')
        print(text_data_json)

        # -----------------------유저가 방에 입장--------------------------- # 나중에 합친 후 변경해야 함
        if text_data_json['send_type'] == 'enter':
            userName = text_data_json['user_name']
            roomName = text_data_json['room_name']
            if roomName not in room:
                room[roomName] = {}
                user_score[roomName] = {}
                room_turn[roomName] = {'room_turn': 0}

            if roomName in room:
                if len(room[roomName]) == 0: #방에 최초로 입장한 유저 처리
                    room[roomName][userName] = 0
                    user_score[roomName][userName] = 0
                    print(room.get(roomName))

                elif len(room[roomName]) == 1: #그 이후로 방에 입장한 유저 처리
                    for key, value in room[roomName].items():
                        if key != userName:
                            if value == 0:
                                room[roomName][userName] = 1
                                user_score[roomName][userName] = 0
                                break
                            elif value == 1:
                                room[roomName][userName] = 0
                                user_score[roomName][userName] = 0
                                break
                    
                    #room[roomName][userName] = len(room[roomName])
                    print(room.get(roomName))
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'print_user_name',
                            'user_name': room[roomName],
                        }
                    )
                else:
                    print("consumers enter error")
        #------------------------유저가 방에서 퇴장------------------------
        elif text_data_json['send_type'] == 'close':
            print('close')
            userName = text_data_json['user_name']
            roomName = text_data_json['room_name']
            del room[roomName][userName]
            del user_score[roomName][userName]
            print(room.get(roomName))

        # -----------------------게임 시작---------------------------
        elif text_data_json['send_type'] == 'start':
            userName = text_data_json['user_name']
            roomName = text_data_json['room_name']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_start',
                    'user_name': userName,
                    # 'present_time': presentTime
                }
            )

            #return redirect('chat:game_start', roomName)
            #consumer.py에서 redirect로 뷰의 함수에 접근하는 것은 불가능인듯

        # -----------------------채팅 내용 수신---------------------------
        elif text_data_json['send_type'] == 'message':
            message = text_data_json['message']
            user_name = text_data_json['user_name']
            # presentTime = text_data_json['present_time']
            # "room" 그룹에 메시지 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_name': user_name,
                    # 'present_time': presentTime
                }
            )


        # -----------------------게임 시작---------------------------
        elif text_data_json['send_type'] == 'start':
            userName = text_data_json['user_name']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_start',
                    'user_name': userName,
                    # 'present_time': presentTime
                }
            )




        # -----------------------게임 기능 수신---------------------------
        elif text_data_json['send_type'] == 'dice_roll':
            print('im working')
            # 주사위 굴리기
            room_name = text_data_json['room_name']
            user_name = text_data_json['user_name']
            get_room_user = room.get(room_name)#나중에 합친 후 변경해야 함
            room_user_number = get_room_user.get(user_name)#나중에 합친 후 변경해야 함

            #print(game.test(room_name, user_name))

            # 주사위 굴리기
            if room_turn[room_name]['room_turn'] < 26:
                if room_turn[room_name]['room_turn'] % 2 == get_room_user[user_name]:
                    self.sys.dice_lock = text_data_json['lock_data']
                    if self.sys.roll() == True :
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'dice_roll',
                                'dice': self.sys.dice,
                                'roll_cnt': self.sys.roll_cnt,
                                'user_number': room_user_number + 1,
                                'used_score': self.sys.used_score,
                            }
                        )
                        print('im working!!')

        else:
            # 족보 판별
            room_name = text_data_json['room_name']
            user_name = text_data_json['user_name']
            get_room_user = room.get(room_name)#나중에 합친 후 변경해야 함

            if room_turn[room_name]['room_turn'] % 2 == get_room_user[user_name]:

                unused = False

                if text_data_json['send_type'] == 'game_number':
                    num = text_data_json['dice_num']
                    unused = self.sys.number(num)

                elif text_data_json['send_type'] == 'game_triple':
                    unused = self.sys.triple()

                elif text_data_json['send_type'] == 'game_fourcard':
                    unused = self.sys.fourcard()

                elif text_data_json['send_type'] == 'game_fullhouse':
                    unused = self.sys.fullhouse()

                elif text_data_json['send_type'] == 'game_Sstraight':
                    unused = self.sys.Sstraight()

                elif text_data_json['send_type'] == 'game_Lstraight':
                    unused = self.sys.Lstraight()

                elif text_data_json['send_type'] == 'game_yachu':
                    unused = self.sys.yachu()

                elif text_data_json['send_type'] == 'game_choice':
                    unused = self.sys.choice()

                if unused == True:
                    print('점수 테이블 : ')
                    print(self.sys.score_table)
                    print(self.sys.used_score)

                    if user_name in get_room_user:
                        room_turn[room_name]['room_turn'] += 1
                        user_score[room_name][user_name] = self.sys.score_table[14]
                        print('유저 점수')
                        print(user_score)
                        room_user_number = get_room_user.get(user_name)
                        #게임오버 판별  원래 26
                        if room_turn[room_name]['room_turn'] >= 26:
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'score_table',
                                    'score': self.sys.score_table,
                                    'user_number': room_user_number + 1,
                                    'game_over': True,
                                    'user_score': user_score[room_name],
                                }
                            )
                            print('gameover test')
                            print("여기있는거 실행되나?")
                            del room[room_name]
                            del room_turn[room_name]
                            del user_score[room_name]
                        else:
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'score_table',
                                    'score': self.sys.score_table,
                                    'user_number': room_user_number + 1,
                                    'game_over': False,
                                }
                            )

                        print('기타 정보')
                        print(get_room_user)
                        print(room_turn)
                    #else: 에러처리




    # -----------------HTML로 데이터 전달-----------------------
    # ------------------채팅 메시지 전달------------------------
    # "room" 그룹에서 메시지 수신
    async def chat_message(self, event):
        message = event['message']
        userName = event['user_name']
        # presentTime = event['present_time']

        # 웹 소켓으로 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message,
            'send_type': 'message',
            'user_name': userName,
            # 'present_time': presentTime
        }))

    # ------------------게임 시작 신호 전달------------------------
    # "room" 그룹에서 게임 시작 정보 수신
    async def game_start(self, event):
        userName = event['user_name']
        await self.send(text_data=json.dumps({
            'send_type': 'start',
            'user_name': userName,
        }))

    # 방에 유저 이름들 출력
    # 'user_name': room[roomName],
    async def print_user_name(self, event):
        user_name_arr = event['user_name']
        await self.send(text_data=json.dumps({
            'send_type': 'print_user_name',
            'user_name_arr': user_name_arr,
        }))

    # -------------------게임 기능 전달-------------------------

    async def dice_roll(self, event):
        dice = event['dice']
        roll_cnt = event['roll_cnt']
        user_number = event['user_number']
        room_user_number = event['user_number']
        used_score = event['used_score']
        # 웹 소켓으로 메시지 전송
        await self.send(text_data=json.dumps({
            'send_type': 'dice_roll',
            'type': dice,
            'roll_cnt': roll_cnt,
            'user_number': room_user_number,
            'used_score': used_score,
        }))

    # 점수 표시 ^^^^위에랑 통합하기
    async def score_table(self, event):
        score = event['score']
        room_user_number = event['user_number']
        game_over = event['game_over']
        # 웹 소켓으로 메시지 전송
        if game_over == True:
            user_score = event['user_score']
            await self.send(text_data=json.dumps({
                'send_type': 'score_table',
                'type': score,
                'user_number': room_user_number,
                'game_over' : True,
                'user_score': user_score,
            }))
        else:
            await self.send(text_data=json.dumps({
                'send_type': 'score_table',
                'type': score,
                'user_number': room_user_number,
                'game_over' : False,
            }))
