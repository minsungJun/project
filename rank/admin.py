from django.contrib import admin
from .models import UserRank

# Register your models here.
class UserRankAdmin(admin.ModelAdmin):
    search_fields = ['user']

admin.site.register(UserRank, UserRankAdmin)