from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

# , movie_details, movie_search
from .services import CriticService, MasterpieceService, ToolkitService, VoteService, WatchlistService

from django.contrib.auth.models import User
from .serializers import (
    CriticVoteSerializer,
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

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetails(APIView):

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseView(APIView):
    service = None
    retrieve_serializer = None
    create_serializer = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_param = request.query_params.get('user_id')
        page_param = request.query_params.get('page')
        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Services (list & paginate)
        objects, range = self.service.list(user=user_param)
        page, has_next, start_index, end_index, total_objects = ToolkitService.paginate(
            page_number=page_param, range=range, objects=objects)
        # Serialize
        serialized_data = self.retrieve_serializer(page, many=True)
        # Response
        response = {
            "total": total_objects,
            "from": start_index,
            "to": end_index,
            "is_last_page": not has_next,
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
            platform=payload["platform"],
            user=request.user
        )
        # Response
        return Response(data, status=status_code)

    def delete(self, request):
        user = request.user
        movie_param = request.query_params.get('movie_id')
        data = {}
        status_code = self.service.delete(movie_id=movie_param, user=user)
        if status_code == 404:
            data = {"message": f"Movie {movie_param} not found for user {user}."}
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

    def get(self, request):
        user_param = request.query_params.get('user_id')
        page_param = request.query_params.get('page')
        stars_param = request.query_params.get('stars')
        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if stars_param:
            try:
                int(stars_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Services (list & paginate)
        objects, range = self.service.list(user=user_param, stars=stars_param)
        page, has_next, start_index, end_index, total_objects = ToolkitService.paginate(
            page_number=page_param, range=range, objects=objects)
        # Serialize
        serialized_data = self.retrieve_serializer(page, many=True)
        # Response
        response = {
            "total": total_objects,
            "from": start_index,
            "to": end_index,
            "is_last_page": not has_next,
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
            platform=payload["platform"],
            user=request.user
        )
        # Response
        return Response(data, status=status_code)


class CriticsView(BaseView):
    service = CriticService

    def get(self, request):
        user_param = request.query_params.get('user_id')
        movie_param = request.query_params.get('movie_id')
        page_param = request.query_params.get('page')
        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Service
        if movie_param:
            objects = CriticService.list_by_movie_id_and_aggregate_votes(
                movie=movie_param)
            count = None
            # Serialize
            serialized_data = CriticVoteSerializer(objects, many=True)
        else:
            critics, range = CriticService.list(user=user_param)
            # Paginate
            page, has_next, start_index, end_index, count = ToolkitService.paginate(
                page_number=page_param, range=range, objects=critics)
            # Serialize
            serialized_data = CriticSerializer(page, many=True)
        # Response
        response = {}
        if not movie_param:
            response["total"] = count
            response["from"] = start_index
            response["to"] = end_index
            response["is_last_page"] = not has_next
        response["data"] = serialized_data.data
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
            platform=payload["platform"],
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
