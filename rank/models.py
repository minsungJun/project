from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRank(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_rank',
    )
    total_game = models.IntegerField(default=0)
    win_game = models.IntegerField(default=0)
    lose_game = models.IntegerField(default=0)
    top_score = models.IntegerField(default=0)
    rating = models.IntegerField(default=500)

    def __str__(self) -> str:
        return "{0}".format(self.user)