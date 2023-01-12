import tmdbsimple as tmdb
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from django.contrib.auth.models import User
from marcus.models import Masterpiece, Watchlist

from marcus.serializers import MasterpieceSerializer, WatchlistSerializer

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
            Masterpiece.objects.get(
                Q(user_id=user_id) &
                (Q(movie_id=payload.get('movie_id')) |
                 Q(position=payload.get('position')))
            )
            return {"error": "Movie or Position already exists."}, status.HTTP_400_BAD_REQUEST
        except Masterpiece.DoesNotExist:
            serializer = MasterpieceSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user_id=user_id)
                return {
                    "message": f"Movie {payload.get('movie_id')} with position {payload.get('position')} successfully added to Masterpiece."
                    }, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    def count(*, user_id: int):
        if not user_id:
            return Masterpiece.objects.all().count()
        return Masterpiece.objects.filter(user_id=user_id).count()


class WatchlistService():

    def retrieve(*, user_id: int):
        return Watchlist.objects.filter(user_id=user_id)

    def create(*, payload: dict, user_id: int):
        try:
            # Find row where: user_id & movie_id
            Watchlist.objects.get(
                Q(user_id=user_id) &
                Q(movie_id=payload.get('movie_id'))
            )
            return {"error": f"Movie {payload.get('movie_id')} already exists in Watchlist."}, status.HTTP_400_BAD_REQUEST
        except Watchlist.DoesNotExist:
            serializer = WatchlistSerializer(data=payload)
            if serializer.is_valid():
                serializer.save(user_id=user_id)
                return {"message": f"Movie {payload.get('movie_id')} successfully added to Watchlist."}, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

    def count(*, user_id: int):
        if not user_id:
            return Watchlist.objects.all().count()
        return Watchlist.objects.filter(user_id=user_id).count()
