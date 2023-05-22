from channels.generic.websocket import AsyncWebsocketConsumer
import json
from chat import game_system, game
from channels.db import database_sync_to_async





class ChatConsumer2(AsyncWebsocketConsumer):

    sys = None


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
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
        if text_data_json['send_type'] == 'user_enter':
            userName = text_data_json['user_name']
            
            # "room" 그룹에 메시지 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_enter',
                    'user_name': userName,
                    # 'present_time': presentTime
                }
            )

        #------------------------유저가 방에서 퇴장------------------------
        elif text_data_json['send_type'] == 'close':
            print('close')
            userName = text_data_json['user_name']
            roomName = text_data_json['room_name']
            

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
        
        # -----------------------유저 준비---------------------------
        elif text_data_json['send_type'] == 'ready_click':
            user_name = text_data_json['user_name']
            
            # "room" 그룹에 메시지 전송
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ready_click',
                    'user_name': user_name,
                    # 'present_time': presentTime
                }
            )

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
    
    # ------------------유저 입장 신호 전달------------------------
    # "room" 그룹에서 유저 입장 신호 수신
    async def user_enter(self, event):
        userName = event['user_name']
        await self.send(text_data=json.dumps({
            'send_type': 'user_enter',
            'user_name': userName,
        }))
    
    # ------------------유저 준비 신호 전달------------------------
    # "room" 그룹에서 유저 준비 신호 수신
    async def ready_click(self, event):
        userName = event['user_name']
        await self.send(text_data=json.dumps({
            'send_type': 'ready_click',
            'user_name': userName,
        }))