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


# class WatchlistSerializer(serializers.ModelSerializer):
#     movie_details = serializers.SerializerMethodField()

#     class Meta:
#         model = Watchlist
#         fields = (
#             "movie_id",
#             "movie_name",
#             "platform",
#             "user_name",
#             "platform",
#             "movie_details",
#         )

#     def get_movie_details(self, obj):
#         details = {}
#         if obj.platform == "movie":
#             response = TMDBService.movie_details(obj.movie_id)
#             details["released_date"] = response["release_date"]
#         else:
#             response = TMDBService.tv_details(obj.movie_id)
#             details["released_date"] = response["first_air_date"]
#         details["poster_path"] = response["poster_path"]
#         details["synopsis"] = response["overview"]
#         try:
#             details["backdrop_path"] = response["backdrop_path"]
#             details["director"] = response.get("created_by")[0].get("name")
#         except Exception as e:
#             print("While getting director :", e)

#         return details


# class CreateWatchlistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Watchlist
#         fields = ("movie_id", "movie_name", "platform")


# class CriticVoteSerializer(serializers.Serializer):
#     user_id = serializers.IntegerField()
#     user_name = serializers.CharField()
#     vote = serializers.FloatField()
#     content = serializers.CharField()


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
            "track_id",
            "track_name",
            "artist_id",
            "artist_name",
            "image_url",
            "user",
        )


class CreatePlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = (
            "album_id",
            "album_name",
            "track_id",
            "track_name",
            "artist_id",
            "artist_name",
            "image_url",
        )
