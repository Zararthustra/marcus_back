from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db import models

from django.contrib.auth.models import User
from marcus.models import Critic, Masterpiece, Watchlist, Vote

import io
import xlsxwriter

# from django.db.models import Q

from django.conf import settings
import tmdbsimple as tmdb

tmdb.API_KEY = settings.TMDB_API_KEY


class ToolkitService:
    """
    Toolkit service class
    """

    def paginate(*, page_number: int, range: int, objects: list[object]):
        """
        Returns paginated objects
        """
        if range is None:
            paginated_objects = objects
            page = paginated_objects
            has_next = False
            total_objects = objects.count()
            start_index = 1
            end_index = total_objects
        else:
            paginated_objects = Paginator(objects, range)
            page = paginated_objects.get_page(page_number)
            has_next = page.has_next()
            start_index = page.start_index()
            end_index = page.end_index()
            total_objects = paginated_objects.count

        return page, has_next, start_index, end_index, total_objects


class MasterpieceService:
    """
    Masterpiece service class
    """

    @staticmethod
    def list(*, user: int, tag: str):
        """
        Paginated list (optional : by user)
        """
        range = 10
        masterpieces = Masterpiece.objects.all().order_by("-created_at")

        if user:
            masterpieces = masterpieces.filter(user=user)

        if tag not in ("Tous", None):
            masterpieces = masterpieces.filter(tags__contains=tag)

        return masterpieces, range

    @staticmethod
    def create(*, movie_id: int, movie_name: str, tags: str, platform: str, user: User):
        """
        Create if (user & movie_id) does not exist
        """
        vote, created = Masterpiece.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
                "platform": platform,
                "tags": tags,
            },
        )
        if not created:
            return {
                "error": f"Movie {vote.movie_id} {vote.movie_name} already exists in Masterpiece."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Movie {vote.movie_id} {vote.movie_name} successfully added to Masterpiece."
        }, status.HTTP_201_CREATED

    @staticmethod
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


class WatchlistService:
    """
    Watchlist service class
    """

    @staticmethod
    def list(*, user: int, tag: str):
        """
        Paginated list (optional : by user)
        """
        range = 10
        watchlists = Watchlist.objects.all().order_by("-created_at")

        if user:
            watchlists = watchlists.filter(user=user)

        if tag not in ("Tous", None):
            watchlists = watchlists.filter(tags__contains=tag)

        return watchlists, range

    @staticmethod
    def create(*, movie_id: int, movie_name: str, tags: str, platform: str, user: User):
        """
        Create if (user & movie_id) does not exist
        """
        vote, created = Watchlist.objects.get_or_create(
            user=user,
            movie_id=movie_id,
            defaults={
                "movie_name": movie_name,
                "platform": platform,
                "tags": tags,
            },
        )
        if not created:
            return {
                "error": f"Movie {vote.movie_id} {vote.movie_name} already exists in Watchlist."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Movie {vote.movie_id} {vote.movie_name} successfully added to Watchlist."
        }, status.HTTP_201_CREATED

    @staticmethod
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


class VoteService:
    """
    Vote service class
    """

    @staticmethod
    def list(*, user: int, stars: int, movie_id: int, tag: str):
        """
        Paginated list (optional filters : by user, by stars)
        """
        range = 20
        votes = Vote.objects.all().order_by("-created_at")

        if user:
            votes = votes.filter(user=user)

        if stars:
            votes = votes.filter(value=stars)

        if movie_id:
            votes = votes.filter(movie_id=movie_id)

        if tag not in ("Tous", None):
            votes = votes.filter(tags__contains=tag)

        return votes, range

    @staticmethod
    def create(
        *,
        movie_id: int,
        movie_name: str,
        value: float,
        platform: str,
        tags: str,
        user: User,
    ):
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
                "tags": tags,
            },
        )
        if not created:
            return {
                "error": f"Movie {vote.movie_id} {vote.movie_name} already exists in Vote."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Movie {vote.movie_id} {vote.movie_name} successfully added to Vote."
        }, status.HTTP_201_CREATED

    @staticmethod
    def check_enum_value(*, value: float):
        """
        Check if value is in enum_values
        """
        enum_values = [x * 0.5 for x in range(0, 11)]
        if value in enum_values:
            return True
        return False

    @staticmethod
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


class CriticService:
    """
    Critic service class
    """

    @staticmethod
    def export(*, user: int):
        critics = Critic.objects.all().order_by("-created_at")

        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()

        headers = ["ID", "TMDB ID", "Nom", "Type", "Genres", "Critique", "Date d'ajout"]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        for row_num, critic in enumerate(critics.filter(user=user), start=1):
            worksheet.write(row_num, 0, str(critic.id))
            worksheet.write(row_num, 1, critic.movie_id)
            worksheet.write(row_num, 2, critic.movie_name)
            worksheet.write(row_num, 3, "Série" if critic.platform == "tv" else "Film")
            worksheet.write(row_num, 4, critic.tags)
            worksheet.write(row_num, 5, critic.content)
            worksheet.write(row_num, 6, critic.created_at.strftime("%d-%m-%Y"))

        workbook.close()
        buffer.seek(0)

        return buffer

    @staticmethod
    def list(*, user: int, tag: str):
        """
        Paginated list of critics (optional : by user, by gender_tag)
        """
        range = 10
        critics = Critic.objects.all().order_by("-created_at")

        if user:
            critics = critics.filter(user=user)

        if tag not in ("Tous", None):
            critics = critics.filter(tags__contains=tag)

        return critics, range

    @staticmethod
    def list_by_movie_id_and_aggregate_votes(*, movie: int):
        """
        List Critics by movie_id with associated vote
        """

        critics = Critic.objects.filter(movie_id=movie).order_by("-created_at")
        votes = Vote.objects.filter(movie_id=movie)
        merged_query = []
        for critic in critics:
            data = {}
            data["user_id"] = critic.user_id
            data["user_name"] = critic.user_name
            data["content"] = critic.content
            data["vote"] = None
            if len(votes) > 0:
                for vote in votes:
                    if (critic.movie_id == vote.movie_id) and (
                        critic.user_id == vote.user_id
                    ):
                        data["vote"] = vote.value
            merged_query.append(data)
        return merged_query

    @staticmethod
    def create(
        *,
        movie_id: int,
        movie_name: str,
        content: str,
        platform: str,
        tags: str,
        user: User,
    ):
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
                "tags": tags,
            },
        )
        if not created:
            return {
                "error": f"Movie {critic.movie_id} {critic.movie_name} already exists in Critic."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Movie {critic.movie_id} {critic.movie_name} successfully added to Critic."
        }, status.HTTP_201_CREATED

    @staticmethod
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


class TMDBService:
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
