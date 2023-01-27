from django.conf import settings
from django.db import models
import uuid


class MovieBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True
    )
    movie_id = models.IntegerField()
    movie_name = models.CharField(max_length=100)
    
    class Meta:
        abstract = True
    
    def user_name(self):
        return self.user.username


class Critic(models.Model):
    content = models.CharField(max_length=1000)


class Vote(models.Model):
    value = models.FloatField()


class Masterpiece(MovieBaseModel):
    pass


class Watchlist(models.Model):
    pass