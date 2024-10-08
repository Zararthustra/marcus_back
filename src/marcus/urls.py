from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users", views.Users.as_view()),
    path("users/<int:user_id>", views.UserDetails.as_view()),
    path("masterpieces", views.MasterpiecesView.as_view(), name="masterpieces"),
    path("watchlists", views.WatchlistsView.as_view(), name="watchlists"),
    path("votes", views.VotesView.as_view(), name="votes"),
    path("critics", views.CriticsView.as_view(), name="critics"),
    path("critics/export", views.CriticsExportView.as_view(), name="critics_export"),
]
