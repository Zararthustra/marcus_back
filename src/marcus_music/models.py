import uuid
from django.db import models
from django.conf import settings


class MusicBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    album_id = models.CharField(max_length=100)
    album_name = models.CharField(max_length=100)
    artist_id = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)
    genders = models.CharField(max_length=1000)


class Masterpiece(MusicBaseModel):
    pass


class Critic(MusicBaseModel):
    content = models.CharField(max_length=2000)


class Vote(MusicBaseModel):
    value = models.FloatField()


class Playlist(MusicBaseModel):
    track_id = models.CharField(primary_key=True, max_length=100)
    track_name = models.CharField(max_length=100)
