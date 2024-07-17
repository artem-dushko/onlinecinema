from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    exp_date = models.DateField(default=date(2024, 1, 1))
    is_expired = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} Profile'