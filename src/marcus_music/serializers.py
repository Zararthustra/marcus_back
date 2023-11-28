from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Critic, Masterpiece, Playlist, Vote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class MasterpieceSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Masterpiece
        fields = (
            "id",
            "album_id",
            "album_name",
            "genders",
            "artist_id",
            "artist_name",
            "album_name",
            "image_url",
            "user",
        )


class CreateMasterpieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masterpiece
        fields = ("album_id", "album_name", "artist_id", "artist_name", "image_url")


class CriticSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Critic
        fields = (
            "id",
            "album_id",
            "album_name",
            "content",
            "artist_id",
            "artist_name",
            "image_url",
            "user",
        )


class CreateCriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critic
        fields = (
            "album_id",
            "album_name",
            "content",
            "artist_id",
            "artist_name",
            "image_url",
        )


class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Vote
        fields = (
            "id",
            "album_id",
            "album_name",
            "value",
            "artist_id",
            "artist_name",
            "image_url",
            "user",
        )


class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = (
            "album_id",
            "album_name",
            "value",
            "artist_id",
            "artist_name",
            "image_url",
        )


class PlaylistSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Playlist
        fields = (
            "id",
            "album_id",
            "album_name",
            "genders",
            "artist_id",
            "artist_name",
            "album_name",
            "image_url",
            "user",
        )


class CreatePlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ("album_id", "album_name", "artist_id", "artist_name", "image_url")
