from django.conf import settings
from django.db import models
import uuid


class MovieBaseModel(models.Model):
    PLATFORMS = (("movie", "movie"), ("tv", "tv"))

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    movie_id = models.IntegerField()
    movie_name = models.CharField(max_length=100)
    platform = models.CharField(max_length=50, choices=PLATFORMS)
    tags = models.CharField(max_length=999, null=True)

    class Meta:
        abstract = True

    def user_name(self):
        return self.user.username


class Critic(MovieBaseModel):
    content = models.CharField(max_length=2000)


class Vote(MovieBaseModel):
    value = models.FloatField()


class Masterpiece(MovieBaseModel):
    pass


class Watchlist(MovieBaseModel):
    pass
