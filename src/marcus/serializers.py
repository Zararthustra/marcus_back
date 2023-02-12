from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Masterpiece, Watchlist, Vote, Critic
from .services import TMDBService


class UserSerializer(serializers.ModelSerializer):
    user_critics = serializers.SerializerMethodField()
    user_masterpieces = serializers.SerializerMethodField()
    user_watchlists = serializers.SerializerMethodField()
    user_votes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username',
                  'user_critics', 'user_masterpieces', 'user_watchlists', 'user_votes'
                  )

    def get_user_critics(self, obj):
        return Critic.objects.filter(user=obj.pk).count()

    def get_user_masterpieces(self, obj):
        return Masterpiece.objects.filter(user=obj.pk).count()

    def get_user_watchlists(self, obj):
        return Watchlist.objects.filter(user=obj.pk).count()

    def get_user_votes(self, obj):
        return Vote.objects.filter(user=obj.pk).count()


class MasterpieceSerializer(serializers.ModelSerializer):
    movie_details = serializers.SerializerMethodField()

    class Meta:
        model = Masterpiece
        fields = ('movie_id', 'movie_name', 'user_id',
                  'user_name', 'platform', 'movie_details')

    def get_movie_details(self, obj):
        details = {}
        if (obj.platform == "movie"):
            response = TMDBService.movie_details(obj.movie_id)
            details["released_date"] = response["release_date"]
        else:
            response = TMDBService.tv_details(obj.movie_id)
            details["released_date"] = response["first_air_date"]
        details["poster_path"] = response["poster_path"]
        details["synopsis"] = response["overview"]

        return details


class CreateMasterpieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masterpiece
        fields = ('movie_id', 'movie_name', 'platform')


class WatchlistSerializer(serializers.ModelSerializer):
    movie_details = serializers.SerializerMethodField()

    class Meta:
        model = Watchlist
        fields = ('movie_id', 'movie_name', 'platform',
                  'user_name', 'platform', 'movie_details')

    def get_movie_details(self, obj):
        details = {}
        if (obj.platform == "movie"):
            response = TMDBService.movie_details(obj.movie_id)
            details["released_date"] = response["release_date"]
        else:
            response = TMDBService.tv_details(obj.movie_id)
            details["released_date"] = response["first_air_date"]
        details["poster_path"] = response["poster_path"]
        details["synopsis"] = response["overview"]

        return details


class CreateWatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ('movie_id', 'movie_name', 'platform')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('movie_id', 'movie_name', 'value',
                  'user_id', 'user_name', 'platform')


class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('movie_id', 'movie_name', 'value', 'platform')


class CriticVoteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    vote = serializers.FloatField()
    content = serializers.CharField()


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critic
        fields = ('movie_id', 'movie_name', 'content',
                  'user_id', 'user_name', 'platform')


class CreateCriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critic
        fields = ('movie_id', 'movie_name', 'content', 'platform')
