from rest_framework import status
from django.contrib.auth.models import User

import io
import xlsxwriter

from .models import Critic, Masterpiece, Playlist, Vote


class MasterpieceService:
    """
    Masterpiece service class
    """

    @staticmethod
    def list(*, user: int, page: int):
        """
        Paginated list (optional : by user)
        """
        range = 10
        if not user:
            masterpieces = Masterpiece.objects.all().order_by("-created_at")
        else:
            if not page:
                range = None
            masterpieces = Masterpiece.objects.filter(user=user).order_by("-created_at")
        return masterpieces, range

    @staticmethod
    def create(
        *,
        album_id: str,
        album_name: str,
        user: User,
        artist_id: str,
        artist_name: str,
        image_url: str,
    ):
        """
        Create if (user & album_id) does not exist
        """
        vote, created = Masterpiece.objects.get_or_create(
            user=user,
            album_id=album_id,
            album_name=album_name,
            artist_id=artist_id,
            artist_name=artist_name,
            image_url=image_url,
        )
        if not created:
            return {
                "error": f"Album {vote.album_id} {vote.album_name} already exists in Masterpiece."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Album {vote.album_id} {vote.album_name} successfully added to Masterpiece."
        }, status.HTTP_201_CREATED

    @staticmethod
    def delete(*, id: str, user: str):
        """
        Delete a row by album_id (called by user)
        """
        try:
            masterpiece = Masterpiece.objects.get(user=user, id=id)
            masterpiece.delete()
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

        headers = ["ID", "Album", "Artiste", "Critique", "Date d'ajout"]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        for row_num, critic in enumerate(critics.filter(user=user), start=1):
            worksheet.write(row_num, 0, str(critic.id))
            worksheet.write(row_num, 1, critic.album_name)
            worksheet.write(row_num, 2, critic.artist_name)
            worksheet.write(row_num, 3, critic.content)
            worksheet.write(row_num, 4, critic.created_at.strftime("%d-%m-%Y"))

        workbook.close()
        buffer.seek(0)

        return buffer

    @staticmethod
    def list(*, user: int, page: int, artist_id: str):
        """
        Paginated list (optional : by user)
        """
        range = 10 if page else None
        if user:
            critics = Critic.objects.filter(user=user).order_by("-created_at")
        elif artist_id:
            critics = Critic.objects.filter(artist_id=artist_id)
        else:
            critics = Critic.objects.all().order_by("-created_at")
        return critics, range

    @staticmethod
    def create(
        *,
        album_id: str,
        album_name: str,
        content: str,
        user: User,
        artist_id: str,
        artist_name: str,
        image_url: str,
    ):
        """
        Create if (user & album_id) does not exist
        """
        critic, created = Critic.objects.get_or_create(
            user=user,
            album_id=album_id,
            defaults={
                "album_name": album_name,
                "content": content,
                "artist_id": artist_id,
                "artist_name": artist_name,
                "image_url": image_url,
            },
        )
        if not created:
            return {
                "error": f"Album {critic.album_id} {critic.album_name} already exists in Critic."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Album {critic.album_id} {critic.album_name} successfully added to Critic."
        }, status.HTTP_201_CREATED

    @staticmethod
    def delete(*, id: str, user: str):
        """
        Delete a row by id (called by user)
        """
        try:
            critic = Critic.objects.get(user=user, id=id)
            critic.delete()
            return 204
        except Exception as e:
            print(e)
            return 404


class VoteService:
    """
    Vote service class
    """

    @staticmethod
    def list(*, user: int, page: int, artist_id: str, stars: int):
        """
        Paginated list (optional : by user)
        """
        range = 10 if page else None
        if user:
            if stars:
                votes = Vote.objects.filter(user=user, value=stars).order_by(
                    "-created_at"
                )
            else:
                votes = Vote.objects.filter(user=user).order_by("-created_at")
        elif artist_id:
            votes = Vote.objects.filter(artist_id=artist_id)
        elif stars:
            votes = Vote.objects.filter(value=stars).order_by("-created_at")
            print(votes)
        else:
            votes = Vote.objects.all().order_by("-created_at")
        return votes, range

    @staticmethod
    def create(
        *,
        album_id: str,
        album_name: str,
        value: str,
        user: User,
        artist_id: str,
        artist_name: str,
        image_url: str,
    ):
        """
        Create if (user & album_id) does not exist
        """
        critic, created = Vote.objects.get_or_create(
            user=user,
            album_id=album_id,
            album_name=album_name,
            value=value,
            artist_id=artist_id,
            artist_name=artist_name,
            image_url=image_url,
        )
        if not created:
            return {
                "error": f"Album {critic.album_id} {critic.album_name} already exists in Vote."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Album {critic.album_id} {critic.album_name} successfully added to Vote."
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
    def delete(*, id: str, user: str):
        """
        Delete a row by id (called by user)
        """
        try:
            critic = Vote.objects.get(user=user, id=id)
            critic.delete()
            return 204
        except Exception as e:
            print(e)
            return 404


class PlaylistService:
    """
    Playlist service class
    """

    @staticmethod
    def list(*, user: int, page: int):
        """
        Paginated list (optional : by user)
        """
        range = 10
        if not user:
            critics = Playlist.objects.all().order_by("-created_at")
        else:
            if not page:
                range = None
            critics = Playlist.objects.filter(user=user).order_by("-created_at")
        return critics, range

    @staticmethod
    def create(
        *,
        album_id: str,
        album_name: str,
        user: User,
        artist_id: str,
        artist_name: str,
        image_url: str,
    ):
        """
        Create if (user & album_id) does not exist
        """
        critic, created = Playlist.objects.get_or_create(
            user=user,
            album_id=album_id,
            album_name=album_name,
            artist_id=artist_id,
            artist_name=artist_name,
            image_url=image_url,
        )
        if not created:
            return {
                "error": f"Album {critic.album_name} already exists in Playlist."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Album {critic.album_name} successfully added to Playlist."
        }, status.HTTP_201_CREATED

    @staticmethod
    def delete(*, id: str, user: str):
        """
        Delete a row by id (called by user)
        """
        try:
            critic = Playlist.objects.get(user=user, id=id)
            critic.delete()
            return 204
        except Exception as e:
            print(e)
            return 404
