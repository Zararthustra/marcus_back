from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from .services import CriticService, MasterpieceService, VoteService, WatchlistService, movie_details, movie_search

# from .models import xxx
from django.contrib.auth.models import User
from .serializers import CreateCriticSerializer, CreateVoteSerializer, CriticSerializer, MasterpieceSerializer, UserSerializer, VoteSerializer, WatchlistSerializer
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
        user = request.query_params.get('user_id')
        if not user:
            response = {
                "total": MasterpieceService.count(user=None)
            }
        else:
            masterpieces = MasterpieceService.retrieve(user=user)
            serialized_data = MasterpieceSerializer(masterpieces, many=True)
            response = {
                "total": MasterpieceService.count(user=user),
                "data": serialized_data.data
            }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data, status = MasterpieceService.create(
            payload=request.data, user=request.user)
        return Response(data, status=status)


class WatchlistsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.query_params.get('user_id')
        if not user:
            response = {
                "total": WatchlistService.count(user=None)
            }
        else:
            watchlists = WatchlistService.retrieve(user=user)
            serialized_data = WatchlistSerializer(watchlists, many=True)
            response = {
                "total": WatchlistService.count(user=user),
                "data": serialized_data.data
            }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data, status = WatchlistService.create(
            payload=request.data, user=request.user)
        return Response(data, status=status)


class VotesView(APIView):

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
        votes = VoteService.list(user=user_param)
        # Serialize
        serialized_data = VoteSerializer(votes, many=True)
        # Response
        response = {
            "total": VoteService.count(user=user_param),
            "data": serialized_data.data
        }
        return Response(response, status=status.HTTP_200_OK)

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


class CriticsView(APIView):
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
        critics = CriticService.list(user=user_param)
        # Serialize
        serialized_data = CriticSerializer(critics, many=True)
        # Response
        response = {
            "total": CriticService.count(user=user_param),
            "data": serialized_data.data
        }
        return Response(response, status=status.HTTP_200_OK)

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
