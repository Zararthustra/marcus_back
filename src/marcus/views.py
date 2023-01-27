from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

# , movie_details, movie_search
from .services import CriticService, MasterpieceService, VoteService, WatchlistService

from django.contrib.auth.models import User
from .serializers import (
    UserSerializer,
    CriticSerializer,
    CreateCriticSerializer,
    VoteSerializer,
    CreateVoteSerializer,
    WatchlistSerializer,
    CreateWatchlistSerializer,
    MasterpieceSerializer,
    CreateMasterpieceSerializer
)
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


class BaseView(APIView):
    service = None
    retrieve_serializer = None
    create_serializer = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_param = request.query_params.get('user_id')
        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Service
        objects = self.service.list(user=user_param)
        count = self.service.count(user=user_param)
        # Serialize
        serialized_data = self.retrieve_serializer(objects, many=True)
        # Response
        response = {
            "total": count,
            "data": serialized_data.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        payload = request.data
        # Serialize
        serialized_data = self.create_serializer(data=payload)
        # Validate
        if not serialized_data.is_valid():
            return Response(
                {"error": serialized_data.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Service
        data, status_code = self.service.create(
            movie_id=payload["movie_id"],
            movie_name=payload["movie_name"],
            user=request.user
        )
        # Response
        return Response(data, status=status_code)


class MasterpiecesView(BaseView):
    service = MasterpieceService
    retrieve_serializer = MasterpieceSerializer
    create_serializer = CreateMasterpieceSerializer


class WatchlistsView(BaseView):
    service = WatchlistService
    retrieve_serializer = WatchlistSerializer
    create_serializer = CreateWatchlistSerializer


class VotesView(BaseView):
    service = VoteService
    retrieve_serializer = VoteSerializer
    create_serializer = CreateVoteSerializer

    def post(self, request):
        payload = request.data
        # Serialize
        serialized_data = CreateVoteSerializer(data=payload)
        # Validate
        if not serialized_data.is_valid():
            return Response(
                {"error": serialized_data.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Enum check
        isCorrectValue = VoteService.check_enum_value(
            value=payload.get("value"))
        if not isCorrectValue:
            return Response({
                "error": "Value must be in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]"
            }, status=status.HTTP_400_BAD_REQUEST)
        # Service
        data, status_code = VoteService.create(
            movie_id=payload["movie_id"],
            movie_name=payload["movie_name"],
            value=payload["value"],
            user=request.user
        )
        # Response
        return Response(data, status=status_code)


class CriticsView(BaseView):
    service = CriticService
    retrieve_serializer = CriticSerializer
    create_serializer = CreateCriticSerializer

    def post(self, request):
        payload = request.data
        # Serialize
        serialized_data = CreateCriticSerializer(data=payload)
        # Validate
        if not serialized_data.is_valid():
            return Response(
                {"error": serialized_data.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Service
        data, status_code = CriticService.create(
            movie_id=payload["movie_id"],
            movie_name=payload["movie_name"],
            content=payload["content"],
            user=request.user
        )
        # Response
        return Response(data, status=status_code)


# class MovieSearch(APIView):

#     def get(self, request):
#         query = self.request.query_params.get('movie')
#         page = self.request.query_params.get('page')
#         response = movie_search(query=query, page=page)
#         return Response(response, status=status.HTTP_200_OK)


# class MovieDetails(APIView):

#     def get(self, request, movie_id):
#         response = movie_details(movie_id=movie_id)
#         return Response(response, status=status.HTTP_200_OK)
