from django.contrib import admin
from .models import GameRoom, GameAttend, GameWatch

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    search_fields = ['room_name']

admin.site.register(GameRoom, RoomAdmin)

class GameAttendAdmin(admin.ModelAdmin):
    search_fields = ['gameroom']

admin.site.register(GameAttend, GameAttendAdmin)

class GameWatchAdmin(admin.ModelAdmin):
    search_fields = ['gameroom']

admin.site.register(GameWatch, GameWatchAdmin)

