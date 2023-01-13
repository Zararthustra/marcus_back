from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from .services import CriticService, MasterpieceService, VoteService, WatchlistService, movie_details, movie_search

# from .models import xxx
from django.contrib.auth.models import User
from .serializers import CriticSerializer, MasterpieceSerializer, UserSerializer, VoteSerializer, WatchlistSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(APIView):
    def post(self, request):
        try:
            User.objects.create_user(username=request.data["username"],
                                     password=request.data["password"])
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"BAD_REQUEST": "User might already exist."}, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class Users(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieSearch(APIView):

    def get(self, request):
        query = self.request.query_params.get('movie')
        page = self.request.query_params.get('page')
        response = movie_search(query=query, page=page)
        return Response(response, status=status.HTTP_200_OK)


class MovieDetails(APIView):

    def get(self, request, movie_id):
        response = movie_details(movie_id=movie_id)
        return Response(response, status=status.HTTP_200_OK)


class MasterpiecesView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            response = {
                "total": MasterpieceService.count(user_id=None)
            }
        else:
            masterpieces = MasterpieceService.retrieve(user_id=user_id)
            serialized_data = MasterpieceSerializer(masterpieces, many=True)
            response = {
                "total": MasterpieceService.count(user_id=user_id),
                "data": serialized_data.data
            }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data, status = MasterpieceService.create(
            payload=request.data, user_id=request.user)
        return Response(data, status=status)


class WatchlistsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            response = {
                "total": WatchlistService.count(user_id=None)
            }
        else:
            watchlists = WatchlistService.retrieve(user_id=user_id)
            serialized_data = WatchlistSerializer(watchlists, many=True)
            response = {
                "total": WatchlistService.count(user_id=user_id),
                "data": serialized_data.data
            }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data, status = WatchlistService.create(
            payload=request.data, user_id=request.user)
        return Response(data, status=status)


class VotesView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            response = {
                "total": VoteService.count(user_id=None)
            }
        else:
            votes = VoteService.retrieve(user_id=user_id)
            serialized_data = VoteSerializer(votes, many=True)
            response = {
                "total": VoteService.count(user_id=user_id),
                "data": serialized_data.data
            }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        isCorrectValue = VoteService.check_enum_value(value=request.data.get('value'))
        if not isCorrectValue:
            response = {
            "error": "Value must be in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]"
            }
            status_code=status.HTTP_400_BAD_REQUEST
        else:
            response, status_code = VoteService.create(
                payload=request.data, user_id=request.user)
        return Response(response, status=status_code)


class CriticsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            response = {
                "total": CriticService.count(user_id=None)
            }
        else:
            critics = CriticService.retrieve(user_id=user_id)
            serialized_data = CriticSerializer(critics, many=True)
            response = {
                "total": CriticService.count(user_id=user_id),
                "data": serialized_data.data
            }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data, status = CriticService.create(
            payload=request.data, user_id=request.user)
        return Response(data, status=status)