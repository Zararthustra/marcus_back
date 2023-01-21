from django.conf import settings
from django.db import models
import uuid


class Critic(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, null=True)
    movie_id = models.IntegerField()
    movie_name = models.CharField(max_length=100)

    def user_name(self):
        return self.user.username

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    value = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, null=True)
    movie_id = models.IntegerField()

class Masterpiece(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    position = models.IntegerField()
    movie_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, null=True)

class Watchlist(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    movie_id = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, null=True)

# class Movie(models.Model):
#     id = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=200)
#     synopsis = models.CharField(max_length=1000)
#     image_path = models.CharField(max_length=200)
#     release_date = models.DateField()
#     duration = models.IntegerField()