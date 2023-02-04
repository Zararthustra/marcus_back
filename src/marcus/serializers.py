from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Masterpiece, Watchlist, Vote, Critic


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MasterpieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masterpiece
        fields = ('movie_id', 'movie_name', 'user_id', 'user_name', 'platform')


class CreateMasterpieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masterpiece
        fields = ('movie_id', 'movie_name', 'platform')


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ('movie_id', 'movie_name', 'platform')


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
