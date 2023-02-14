from django import forms
from chat.models import GameRoom

class RoomForm(forms.ModelForm):
    class Meta:
        model = GameRoom
        fields = ['room_name', 'room_url']
        labels = {
            'room_name': '방제',
            'room_url': '방주소',
        }