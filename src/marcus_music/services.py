from rest_framework import status
from django.contrib.auth.models import User

from .models import Critic, Masterpiece, Playlist, Vote


class MasterpieceService:
    """
    Masterpiece service class
    """

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

    def create(
        *,
        album_id: str,
        album_name: str,
        user: User,
        genders: str,
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
            genders=genders,
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

    def list(*, user: int, page: int, artist_id: str):
        """
        Paginated list (optional : by user)
        """
        range = 10 if page else None
        if user:
            critics = Vote.objects.filter(user=user).order_by("-created_at")
        elif artist_id:
            critics = Vote.objects.filter(artist_id=artist_id)
        else:
            critics = Vote.objects.all().order_by("-created_at")
        return critics, range

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

    def create(
        *,
        album_id: str,
        album_name: str,
        user: User,
        artist_id: str,
        artist_name: str,
        image_url: str,
        track_id: str,
        track_name: str,
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
            track_id=track_id,
            track_name=track_name,
        )
        if not created:
            return {
                "error": f"Track {critic.track_name} already exists in Playlist."
            }, status.HTTP_400_BAD_REQUEST
        return {
            "message": f"Track {critic.track_name} successfully added to Playlist."
        }, status.HTTP_201_CREATED

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
