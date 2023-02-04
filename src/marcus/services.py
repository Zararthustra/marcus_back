import json
from rest_framework import status

from django.contrib.auth.models import User
from marcus.models import Critic, Masterpiece, Watchlist, Vote

# from django.shortcuts import get_object_or_404
# from django.db.models import Q


class MasterpieceService():
    """
        Masterpiece service class
    """

    def list(*, user: int):
        """
            List by user
        """
        if not user:
            return Masterpiece.objects.all()
        return Masterpiece.objects.filter(user=user)

    def create(*, movie_id: int, movie_name: str, user: User):
        """
            Create if (user & movie_id) does not exist
        """
        vote, created = Masterpiece.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
            }
        )
        if not created:
            return {
                "error": f"Movie {vote.movie_id} {vote.movie_name} already exists in Masterpiece."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Movie {vote.movie_id} {vote.movie_name} successfully added to Masterpiece."
        }, status.HTTP_201_CREATED

    def count(*, user: int):
        """
            Count all rows or by user
        """
        if not user:
            return Masterpiece.objects.all().count()
        return Masterpiece.objects.filter(user=user).count()


class WatchlistService():
    """
        Watchlist service class
    """

    def list(*, user: int):
        """
            List by user
        """
        if not user:
            return Watchlist.objects.all()
        return Watchlist.objects.filter(user=user)

    def create(*, movie_id: int, movie_name: str, user: User):
        """
            Create if (user & movie_id) does not exist
        """
        vote, created = Watchlist.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
            }
        )
        if not created:
            return {
                "error": f"Movie {vote.movie_id} {vote.movie_name} already exists in Watchlist."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Movie {vote.movie_id} {vote.movie_name} successfully added to Watchlist."
        }, status.HTTP_201_CREATED

    def count(*, user: int):
        """
            Count all rows or by user
        """
        if not user:
            return Watchlist.objects.all().count()
        return Watchlist.objects.filter(user=user).count()


class VoteService():
    """
        Vote service class
    """

    def list(*, user: int):
        """
            List by user
        """
        if not user:
            return Vote.objects.all()
        return Vote.objects.filter(user=user)

    def create(*, movie_id: int, movie_name: str, value: float, user: User):
        """
            Create if (user & movie_id) does not exist
        """
        vote, created = Vote.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
                "value": value,
            }
        )
        if not created:
            return {
                "error": f"Movie {vote.movie_id} {vote.movie_name} already exists in Vote."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Movie {vote.movie_id} {vote.movie_name} successfully added to Vote."
        }, status.HTTP_201_CREATED

    def count(*, user: int):
        """
            Count all rows or by user
        """
        if not user:
            return Vote.objects.all().count()
        return Vote.objects.filter(user=user).count()

    def check_enum_value(*, value: float):
        """
            Check if value is in enum_values
        """
        enum_values = [x * 0.5 for x in range(0, 11)]
        if value in enum_values:
            return True
        return False


class CriticService():
    """
        Critic service class
    """

    def list(*, user: int):
        """
            Optional List by user or movie
        """
        if user:
            return Critic.objects.filter(user=user)
        return Critic.objects.all()

    def list_by_movie_id_and_aggregate_votes(*, movie: int):
        """
            List Critics by movie_id with associated vote
        """

        critics = Critic.objects.filter(movie_id=movie)
        votes = Vote.objects.filter(movie_id=movie)
        merged_query = []
        for critic in critics:
            data = {}
            data["user_id"] = critic.user_id
            data["user_name"] = critic.user_name
            data["content"] = critic.content
            data["vote"] = None
            if (len(votes) > 0):
                for vote in votes:
                    if (critic.movie_id == vote.movie_id) and (critic.user_id == vote.user_id):
                        data["vote"] = vote.value
            merged_query.append(data)
        return merged_query

    def create(*, movie_id: int, movie_name: str, content: str, user: User):
        """
            Create if (user & movie_id) does not exist
        """
        critic, created = Critic.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
                "content": content,
            }
        )
        if not created:
            return {
                "error": f"Movie {critic.movie_id} {critic.movie_name} already exists in Critic."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Movie {critic.movie_id} {critic.movie_name} successfully added to Critic."
        }, status.HTTP_201_CREATED

    def count(*, user: int):
        """
            Count all rows or by user
        """
        if not user:
            return Critic.objects.all().count()
        return Critic.objects.filter(user=user).count()


# from django.conf import settings
# import tmdbsimple as tmdb
# tmdb.API_KEY = settings.TMDB_API_KEY

# def movie_search(query: str, page=int):
#     search = tmdb.Search()
#     response = search.movie(query=query, language="fr", page=page)
#     return response


# def movie_details(movie_id: int):
#     movie = tmdb.Movies(movie_id)
#     response = movie.info(language="fr")
#     return response
