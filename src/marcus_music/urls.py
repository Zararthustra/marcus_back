from django.urls import path
from . import views

urlpatterns = [
    path("masterpieces", views.MasterpiecesView.as_view()),
    path("playlists", views.PlaylistsView.as_view()),
    path("votes", views.VotesView.as_view()),
    path("critics", views.CriticsView.as_view()),
]
