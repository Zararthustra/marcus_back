from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status

from .services import movie_details, search_movie

# from .models import xxx
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404


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

class SearchMovie(APIView):

    def get(self, request):
        query = self.request.query_params.get('movie')
        page = self.request.query_params.get('page')
        response = search_movie(query=query, page=page)
        return Response(response, status=status.HTTP_200_OK)

class MovieDetails(APIView):

    def get(self, request, movie_id):
        response = movie_details(movie_id=movie_id)
        return Response(response, status=status.HTTP_200_OK)