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
        fields = ('movie_id', 'movie_name', 'user_id', 'user_name')

class CreateMasterpieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masterpiece
        fields = ('movie_id', 'movie_name')


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ('movie_id', 'movie_name')

class CreateWatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ('movie_id', 'movie_name')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('movie_id', 'movie_name', 'value', 'user_id', 'user_name')

class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('movie_id', 'movie_name', 'value')


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critic
        fields = ('movie_id', 'movie_name', 'content', 'user_id', 'user_name')

class CreateCriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critic
        fields = ('movie_id', 'movie_name', 'content')