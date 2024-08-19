from django.urls import path
from . import views

urlpatterns = [
    path("masterpieces", views.MasterpiecesView.as_view(), name="music_masterpieces"),
    path("playlists", views.PlaylistsView.as_view(), name="music_playlists"),
    path("votes", views.VotesView.as_view(), name="music_votes"),
    path("critics", views.CriticsView.as_view(), name="music_critics"),
    path(
        "critics/export", views.CriticsExportView.as_view(), name="music_critics_export"
    ),
]
