from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Masterpiece, Watchlist, Vote, Critic
from marcus_music.models import (
    Masterpiece as MusicMasterpiece,
    Playlist,
    Vote as MusicVote,
    Critic as MusicCritic,
)
from .services import TMDBService


class UserSerializer(serializers.ModelSerializer):
    user_critics = serializers.SerializerMethodField()
    user_masterpieces = serializers.SerializerMethodField()
    user_watchlists = serializers.SerializerMethodField()
    user_votes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "user_critics",
            "user_masterpieces",
            "user_watchlists",
            "user_votes",
        )

    def get_user_critics(self, obj):
        movie_critics = Critic.objects.filter(user=obj.pk).count()
        music_critics = MusicCritic.objects.filter(user=obj.pk).count()

        return movie_critics + music_critics

    def get_user_masterpieces(self, obj):
        movie_masterpieces = Masterpiece.objects.filter(user=obj.pk).count()
        music_masterpieces = MusicMasterpiece.objects.filter(user=obj.pk).count()

        return movie_masterpieces + music_masterpieces

    def get_user_watchlists(self, obj):
        watchlists = Watchlist.objects.filter(user=obj.pk).count()
        playlists = Playlist.objects.filter(user=obj.pk).count()

        return watchlists + playlists

    def get_user_votes(self, obj):
        movie_votes = Vote.objects.filter(user=obj.pk).count()
        music_votes = MusicVote.objects.filter(user=obj.pk).count()

        return movie_votes + music_votes


class MasterpieceSerializer(serializers.ModelSerializer):
    movie_details = serializers.SerializerMethodField()

    class Meta:
        model = Masterpiece
        fields = (
            "movie_id",
            "movie_name",
            "user_id",
            "user_name",
            "platform",
            "movie_details",
        )

    def get_movie_details(self, obj):
        details = {}
        if obj.platform == "movie":
            response = TMDBService.movie_details(obj.movie_id)
            details["released_date"] = response["release_date"]
        else:
            response = TMDBService.tv_details(obj.movie_id)
            details["released_date"] = response["first_air_date"]
        details["poster_path"] = response["poster_path"]
        details["synopsis"] = response["overview"]
        try:
            details["backdrop_path"] = response["backdrop_path"]
            details["director"] = response.get("created_by")[0].get("name")
        except Exception as e:
            print("While getting director :", e)
        return details


class CreateMasterpieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masterpiece
        fields = ("movie_id", "movie_name", "platform")


class WatchlistSerializer(serializers.ModelSerializer):
    movie_details = serializers.SerializerMethodField()

    class Meta:
        model = Watchlist
        fields = (
            "movie_id",
            "movie_name",
            "platform",
            "user_name",
            "user_id",
            "platform",
            "movie_details",
        )

    def get_movie_details(self, obj):
        details = {}
        if obj.platform == "movie":
            response = TMDBService.movie_details(obj.movie_id)
            details["released_date"] = response["release_date"]
        else:
            response = TMDBService.tv_details(obj.movie_id)
            details["released_date"] = response["first_air_date"]
        details["poster_path"] = response["poster_path"]
        details["synopsis"] = response["overview"]
        try:
            details["backdrop_path"] = response["backdrop_path"]
            details["director"] = response.get("created_by")[0].get("name")
        except Exception as e:
            print("While getting director :", e)

        return details


class CreateWatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ("movie_id", "movie_name", "platform")


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("movie_id", "movie_name", "value", "user_id", "user_name", "platform")


class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("movie_id", "movie_name", "value", "platform")


class CriticVoteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    vote = serializers.FloatField()
    content = serializers.CharField()


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critic
        fields = (
            "movie_id",
            "movie_name",
            "content",
            "user_id",
            "user_name",
            "platform",
        )


class CreateCriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critic
        fields = ("movie_id", "movie_name", "content", "platform")
