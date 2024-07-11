from django.contrib.auth.models import User
from django.db import models
from cinema.models import Video

class WatchList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video)

    def __str__(self):
        return f'{self.user.username} WatchList'