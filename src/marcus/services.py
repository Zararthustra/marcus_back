import tmdbsimple as tmdb
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from django.contrib.auth.models import User
from marcus.models import Critic, Masterpiece, Watchlist, Vote

from marcus.serializers import CriticSerializer, MasterpieceSerializer, WatchlistSerializer, VoteSerializer

tmdb.API_KEY = settings.TMDB_API_KEY


def movie_search(query: str, page=int):
    search = tmdb.Search()
    response = search.movie(query=query, language="fr", page=page)
    return response


def movie_details(movie_id: int):
    movie = tmdb.Movies(movie_id)
    response = movie.info(language="fr")
    return response


class MasterpieceService():
    """
        Masterpiece service class
    """

    def retrieve(*, user: int):
        """
            Retrieve by user
        """
        return Masterpiece.objects.filter(user=user)

    def create(*, payload: dict, user: int):
        """
            Create if not exist
        """

        try:
            # Find row where: user & (movie_id | position)
            masterpiece = Masterpiece.objects.get(
                Q(user=user) &
                (Q(movie_id=payload.get('movie_id')) |
                 Q(position=payload.get('position')))
            )
            return {"error": f"Movie {masterpiece.movie_id} with Position {masterpiece.position} already exists."}, status.HTTP_400_BAD_REQUEST
        except Masterpiece.DoesNotExist:
            serializer = MasterpieceSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user=user)
                return {
                    "message": f"Movie {payload.get('movie_id')} with Position {payload.get('position')} successfully added to Masterpiece."
                }, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

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

    def retrieve(*, user: int):
        """
            Retrieve by user
        """
        return Watchlist.objects.filter(user=user)

    def create(*, payload: dict, user: int):
        """
            Create if not exist
        """
        try:
            # Find row where: user & movie_id
            watchlist = Watchlist.objects.get(
                Q(user=user) &
                Q(movie_id=payload.get('movie_id'))
            )
            return {
                "error": f"Movie {watchlist.movie_id} already exists in Watchlist."
            }, status.HTTP_400_BAD_REQUEST
        except Watchlist.DoesNotExist:
            serializer = WatchlistSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user=user)
                return {
                    "message": f"Movie {payload.get('movie_id')} successfully added to Watchlist."
                }, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

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

    def retrieve(*, user: int):
        """
            Retrieve by user
        """
        return Vote.objects.filter(user=user)

    def create(*, payload: dict, user: int):
        """
            Create if not exist
        """
        try:
            # Find row where: user & movie_id
            vote = Vote.objects.get(
                Q(user=user) &
                Q(movie_id=payload.get('movie_id'))
            )
            return {
                "error": f"Movie {vote.movie_id} with value {vote.value} already exists in Vote."
            }, status.HTTP_400_BAD_REQUEST
        except Vote.DoesNotExist:
            serializer = VoteSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user=user)
                return {
                    "message": f"Movie {payload.get('movie_id')} with Value {payload.get('value')} successfully added to Vote."
                }, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

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
        print(enum_values)
        if value in enum_values:
            return True
        return False


class CriticService():
    """
        Critic service class
    """

    def list(*, user: int):
        """
            List by user
        """
        if not user:
            return Critic.objects.all()
        return Critic.objects.filter(user=user)

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
