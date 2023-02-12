import json
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from marcus.models import Critic, Masterpiece, Watchlist, Vote

# from django.db.models import Q

from django.conf import settings
import tmdbsimple as tmdb
tmdb.API_KEY = settings.TMDB_API_KEY


class MasterpieceService():
    """
        Masterpiece service class
    """

    def list(*, user: int):
        """
            List by user
        """
        if not user:
            return Masterpiece.objects.all().order_by('-created_at')
        return Masterpiece.objects.filter(user=user).order_by('-created_at')

    def create(*, movie_id: int, movie_name: str, platform: str, user: User):
        """
            Create if (user & movie_id) does not exist
        """
        vote, created = Masterpiece.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
                "platform": platform,
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

    def delete(*, movie_id: int, user: str):
        """
            Delete a row by movie_id (called by user)
        """
        try:
            masterpiece = Masterpiece.objects.get(user=user, movie_id=movie_id)
            masterpiece.delete()
            return 204
        except Exception as e:
            print(e)
            return 404


class WatchlistService():
    """
        Watchlist service class
    """

    def list(*, user: int):
        """
            List by user
        """
        if not user:
            return Watchlist.objects.all().order_by('-created_at')
        return Watchlist.objects.filter(user=user).order_by('-created_at')

    def create(*, movie_id: int, movie_name: str, platform: str, user: User):
        """
            Create if (user & movie_id) does not exist
        """
        vote, created = Watchlist.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
                "platform": platform,
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

    def delete(*, movie_id: int, user: str):
        """
            Delete a row by movie_id (called by user)
        """
        try:
            watchlist = Watchlist.objects.get(user=user, movie_id=movie_id)
            watchlist.delete()
            return 204
        except Exception as e:
            print(e)
            return 404


class VoteService():
    """
        Vote service class
    """

    def list(*, user: int):
        """
            List by user
        """
        if not user:
            return Vote.objects.all().order_by('-created_at')
        return Vote.objects.filter(user=user).order_by('-created_at')

    def create(*, movie_id: int, movie_name: str, value: float, platform: str, user: User):
        """
            Create if (user & movie_id) does not exist
        """
        vote, created = Vote.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
                "platform": platform,
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

    def delete(*, movie_id: int, user: str):
        """
            Delete a row by movie_id (called by user)
        """
        try:
            vote = Vote.objects.get(user=user, movie_id=movie_id)
            vote.delete()
            return 204
        except Exception as e:
            print(e)
            return 404


class CriticService():
    """
        Critic service class
    """

    def list(*, user: int):
        """
            Optional List by user or movie
        """
        if user:
            return Critic.objects.filter(user=user).order_by('-created_at')
        return Critic.objects.all().order_by('-created_at')

    def list_by_movie_id_and_aggregate_votes(*, movie: int):
        """
            List Critics by movie_id with associated vote
        """

        critics = Critic.objects.filter(movie_id=movie).order_by('-created_at')
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

    def create(*, movie_id: int, movie_name: str, content: str, platform: str, user: User):
        """
            Create if (user & movie_id) does not exist
        """
        critic, created = Critic.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
                "content": content,
                "platform": platform,
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

    def delete(*, movie_id: int, user: str):
        """
            Delete a row by movie_id (called by user)
        """
        try:
            critic = Critic.objects.get(user=user, movie_id=movie_id)
            critic.delete()
            return 204
        except Exception as e:
            print(e)
            return 404


class TMDBService():
    """
        TMDB service class
    """

    def movie_details(movie_id: int):
        movie = tmdb.Movies(movie_id)
        response = movie.info(language="fr")
        return response

    def tv_details(movie_id: int):
        movie = tmdb.TV(movie_id)
        response = movie.info(language="fr")
        return response
