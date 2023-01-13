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

    def retrieve(*, user_id: int):
        return Masterpiece.objects.filter(user_id=user_id)

    def create(*, payload: dict, user_id: int):
        """
            Create if not exist
        """

        try:
            # Find row where: user_id & (movie_id | position)
            masterpiece = Masterpiece.objects.get(
                Q(user_id=user_id) &
                (Q(movie_id=payload.get('movie_id')) |
                 Q(position=payload.get('position')))
            )
            return {"error": f"Movie {masterpiece.movie_id} with Position {masterpiece.position} already exists."}, status.HTTP_400_BAD_REQUEST
        except Masterpiece.DoesNotExist:
            serializer = MasterpieceSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user_id=user_id)
                return {
                    "message": f"Movie {payload.get('movie_id')} with Position {payload.get('position')} successfully added to Masterpiece."
                }, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    def count(*, user_id: int):
        if not user_id:
            return Masterpiece.objects.all().count()
        return Masterpiece.objects.filter(user_id=user_id).count()


class WatchlistService():
    """
            Create if not exist
    """

    def retrieve(*, user_id: int):
        return Watchlist.objects.filter(user_id=user_id)

    def create(*, payload: dict, user_id: int):
        try:
            # Find row where: user_id & movie_id
            watchlist = Watchlist.objects.get(
                Q(user_id=user_id) &
                Q(movie_id=payload.get('movie_id'))
            )
            return {
                "error": f"Movie {watchlist.movie_id} already exists in Watchlist."
            }, status.HTTP_400_BAD_REQUEST
        except Watchlist.DoesNotExist:
            serializer = WatchlistSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user_id=user_id)
                return {
                    "message": f"Movie {payload.get('movie_id')} successfully added to Watchlist."
                }, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    def count(*, user_id: int):
        if not user_id:
            return Watchlist.objects.all().count()
        return Watchlist.objects.filter(user_id=user_id).count()


class VoteService():
    """
            Create if not exist
    """

    def retrieve(*, user_id: int):
        return Vote.objects.filter(user_id=user_id)

    def create(*, payload: dict, user_id: int):
        try:
            # Find row where: user_id & movie_id
            vote = Vote.objects.get(
                Q(user_id=user_id) &
                Q(movie_id=payload.get('movie_id'))
            )
            return {
                "error": f"Movie {vote.movie_id} with value {vote.value} already exists in Vote."
            }, status.HTTP_400_BAD_REQUEST
        except Vote.DoesNotExist:
            serializer = VoteSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user_id=user_id)
                return {
                    "message": f"Movie {payload.get('movie_id')} with Value {payload.get('value')} successfully added to Vote."
                }, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    def count(*, user_id: int):
        if not user_id:
            return Vote.objects.all().count()
        return Vote.objects.filter(user_id=user_id).count()
    
    def check_enum_value(*, value: float):
        enum_values = [x * 0.5 for x in range(0, 11)]
        print(enum_values)
        if value in enum_values:
            return True
        return False


class CriticService():
    """
            Create if not exist
    """

    def retrieve(*, user_id: int):
        return Critic.objects.filter(user_id=user_id)

    def create(*, payload: dict, user_id: int):
        try:
            # Find row where: user_id & movie_id
            critic = Critic.objects.get(
                Q(user_id=user_id) &
                Q(movie_id=payload.get('movie_id'))
            )
            return {
                "error": f"Movie {critic.movie_id} already exists in Critic."
            }, status.HTTP_400_BAD_REQUEST
        except Critic.DoesNotExist:
            serializer = CriticSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user_id=user_id)
                return {
                    "message": f"Movie {payload.get('movie_id')} successfully added to Critic."
                }, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    def count(*, user_id: int):
        if not user_id:
            return Critic.objects.all().count()
        return Critic.objects.filter(user_id=user_id).count()