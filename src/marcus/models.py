from django.conf import settings
from django.db import models
import uuid


class Critic(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    content = models.CharField(max_length=1000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    movie_id = models.IntegerField(unique=True)

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    value = models.IntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    movie_id = models.IntegerField(unique=True)

class Masterpiece(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    movie_id = models.IntegerField(unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

class Watchlist(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    movie_id = models.IntegerField(unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)

# class Movie(models.Model):
#     id = models.IntegerField(primary_key=True)
#     title = models.CharField(max_length=200)
#     synopsis = models.CharField(max_length=1000)
#     image_path = models.CharField(max_length=200)
#     release_date = models.DateField()
#     duration = models.IntegerField()