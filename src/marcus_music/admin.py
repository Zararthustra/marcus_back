from django.contrib import admin
from .models import (
    Masterpiece as MusicMasterpiece,
    Playlist,
    Vote as MusicVote,
    Critic as MusicCritic,
)

admin.site.register(MusicCritic)
admin.site.register(MusicVote)
admin.site.register(Playlist)
admin.site.register(MusicMasterpiece)
