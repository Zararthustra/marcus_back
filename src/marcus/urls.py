from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users', views.Users.as_view()),
    
    path('movies', views.MovieSearch.as_view()),
    path('movies/<int:movie_id>', views.MovieDetails.as_view()),

    path('masterpieces', views.MasterpiecesView.as_view()),
    # path('masterpieces/<int:masterpiece_id>', views.MasterpieceView.as_view()),

    path('watchlists', views.WatchlistsView.as_view()),

    path('votes', views.VotesView.as_view()),

    path('critics', views.CriticsView.as_view()),
]