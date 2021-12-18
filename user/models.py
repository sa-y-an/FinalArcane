from django.db import models
# from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass



class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    email = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=200, blank=True)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    last_submit = models.DateTimeField(
        default=datetime.utcnow()+timedelta(hours=5.5))
    question_level = models.IntegerField(default=1)
    level2 = models.IntegerField(default=-2)
    count2 = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class PlayerDetails(models.Model):
    user_name = models.OneToOneField(
        Player, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(default="your name", max_length=400)
    college = models.CharField(default="none", max_length=400)
    year = models.CharField(default="1", max_length=10)
    contact = models.BigIntegerField(default=1, blank=True)

    def __str__(self):
        return self.college


class Solved(models.Model):
    gamer = models.ForeignKey(Player, on_delete=models.CASCADE)
    level_on = models.IntegerField(default=0, blank=True)
    solved = models.BooleanField(default=False)


class StageOneHint(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.IntegerField(default=0, blank=True)
    taken = models.BooleanField(default=False)
