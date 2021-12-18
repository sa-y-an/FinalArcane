from django.db import models

# Create your models here.


class Leaders(models.Model):
    cutoffScore = models.IntegerField(default=10)
