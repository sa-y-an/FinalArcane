from django.db import models

# Create your models here.

# static questions containing only text and images
desc = " the images related to a Doc are retrieved by the images property of doc which is generated from the related_name attribute in the ForeignKey"

class Stage_1(models.Model):
    title = models.CharField(blank=True, max_length=200)
    level = models.IntegerField(unique=True)
    description = models.TextField(blank=True, default=desc)
    image_url = models.URLField(blank=True)
    hint = models.TextField(blank=True, default='hint')
    answer = models.CharField(blank=True, max_length=400)
    format = models.CharField(blank=True, max_length=200)

    def __str__(self):
        return str(str(self.level)+str(" . ")+str(self.title))


class StageTwo(models.Model):
    title = models.CharField(blank=True, max_length=200)
    description = models.TextField(blank=True, default=desc)
    answer = models.CharField(blank=True, max_length=400)
    level = models.IntegerField(unique=True)
    image_url = models.URLField(blank=True)
    format = models.CharField(blank=True, max_length=200)
    audio_url = models.URLField(blank=True)

    def __str__(self):
        return str(str(self.level)+str(" . ")+str(self.title))
