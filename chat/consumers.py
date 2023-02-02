from channels.generic.websocket import AsyncWebsocketConsumer
import json
from chat import game_system

room = {}


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

        # -----------------------유저가 방에 입장---------------------------
        if text_data_json['send_type'] == 'enter':
            userName = text_data_json['user_name']
            roomName = text_data_json['room_name']
            if roomName not in room:
                room[roomName] = {'room_turn': 0}

                # print(len(room[roomName]))
                # print(room.get(roomName))
            if roomName in room:
                if len(room[roomName]) < 3:
                    room[roomName][userName] = len(room[roomName])-1

                    # print(len(room[roomName]))
                    print(room.get(roomName))
                else:
                    print("error")

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


        # -----------------------게임 기능 수신---------------------------
        elif text_data_json['send_type'] == 'dice_roll':
            # 주사위 굴리기
            room_name = text_data_json['room_name']
            user_name = text_data_json['user_name']
            get_room_user = room.get(room_name)

            if get_room_user['room_turn'] % 2 == get_room_user[user_name]:
                self.sys.dice_lock = text_data_json['lock_data']
                self.sys.roll()
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'dice_roll',
                        'dice': self.sys.dice,
                        'roll_cnt': self.sys.roll_cnt,
                    }
                )

        else:
            # 족보 판별
            room_name = text_data_json['room_name']
            user_name = text_data_json['user_name']
            get_room_user = room.get(room_name)

            if get_room_user['room_turn'] % 2 == get_room_user[user_name]:
                if text_data_json['send_type'] == 'game_number':
                    num = text_data_json['dice_num']
                    self.sys.number(num)
                elif text_data_json['send_type'] == 'game_triple':
                    self.sys.triple()

                elif text_data_json['send_type'] == 'game_fourcard':
                    self.sys.fourcard()

                elif text_data_json['send_type'] == 'game_fullhouse':
                    self.sys.fullhouse()

                elif text_data_json['send_type'] == 'game_Sstraight':
                    self.sys.Sstraight()

                elif text_data_json['send_type'] == 'game_Lstraight':
                    self.sys.Lstraight()

                elif text_data_json['send_type'] == 'game_yachu':
                    self.sys.yachu()

                elif text_data_json['send_type'] == 'game_choice':
                    self.sys.choice()

                print('점수 테이블 : ')
                print(self.sys.score_table)

                if user_name in get_room_user:
                    room_user_number = get_room_user.get(user_name)
                    if room_user_number == 0:
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'score_table',
                                'score': self.sys.score_table,
                                'user_number': 1,
                            }
                        )
                    else:
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'score_table',
                                'score': self.sys.score_table,
                                'user_number': 2,
                            }
                        )
                    get_room_user['room_turn'] += 1
                    print(get_room_user)
                #else: 에러처리



    # -----------------HTML로 데이터 전달-----------------------
    # ------------------채팅 메시지 전달-------------------------
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

    # -------------------게임 기능 전달-------------------------

    async def dice_roll(self, event):
        dice = event['dice']
        roll_cnt = event['roll_cnt']
        user_number = event['user_number']
        # 웹 소켓으로 메시지 전송
        await self.send(text_data=json.dumps({
            'send_type': 'dice_roll',
            'type': dice,
            'roll_cnt': roll_cnt,
            'user_number': user_number,
        }))

    # 점수 표시
    async def score_table(self, event):
        score = event['score']
        user_number = event['user_number']
        # 웹 소켓으로 메시지 전송
        await self.send(text_data=json.dumps({
            'send_type': 'score_table',
            'type': score,
            'user_number': user_number,
        }))
