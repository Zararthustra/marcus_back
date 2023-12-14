from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from marcus.services import ToolkitService
from marcus_music.serializers import (
    CreateCriticSerializer,
    CreateMasterpieceSerializer,
    CreatePlaylistSerializer,
    CreateVoteSerializer,
    CriticSerializer,
    MasterpieceSerializer,
    PlaylistSerializer,
    VoteSerializer,
)
from marcus_music.services import (
    CriticService,
    MasterpieceService,
    PlaylistService,
    VoteService,
)


class BaseView(APIView):
    service = None
    retrieve_serializer = None
    create_serializer = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user_param = request.query_params.get("user_id")
        artist_param = request.query_params.get("artist_id")
        page_param = request.query_params.get("page")
        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Services (list & paginate)
        objects, range = self.service.list(
            user=user_param, page=page_param, artist_id=artist_param
        )
        page, has_next, start_index, end_index, total_objects = ToolkitService.paginate(
            page_number=page_param, range=range, objects=objects
        )
        # Serialize
        serialized_data = self.retrieve_serializer(page, many=True)
        # Response
        response = {
            "total": total_objects,
            "from": start_index,
            "to": end_index,
            "is_last_page": not has_next,
            "data": serialized_data.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        payload = request.data
        # Serialize
        serialized_data = self.create_serializer(data=payload)
        # Validate
        if not serialized_data.is_valid():
            return Response(
                {"error": serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        # Service
        data, status_code = self.service.create(
            album_id=payload["album_id"],
            album_name=payload["album_name"],
            artist_id=payload["artist_id"],
            artist_name=payload["artist_name"],
            image_url=payload["image_url"],
            genders=payload["genders"],
            user=request.user,
        )
        # Response
        return Response(data, status=status_code)

    def delete(self, request):
        user = request.user
        music_param = request.query_params.get("id")
        data = {}
        status_code = self.service.delete(id=music_param, user=user)
        if status_code == 404:
            data = {"message": f"Music {music_param} not found for user {user}."}
        return Response(data, status=status_code)


class MasterpiecesView(BaseView):
    service = MasterpieceService
    retrieve_serializer = MasterpieceSerializer
    create_serializer = CreateMasterpieceSerializer

    def get(self, request):
        user_param = request.query_params.get("user_id")
        page_param = request.query_params.get("page")
        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Services (list & paginate)
        objects, range = self.service.list(user=user_param, page=page_param)
        page, has_next, start_index, end_index, total_objects = ToolkitService.paginate(
            page_number=page_param, range=range, objects=objects
        )
        # Serialize
        serialized_data = self.retrieve_serializer(page, many=True)
        # Response
        response = {
            "total": total_objects,
            "from": start_index,
            "to": end_index,
            "is_last_page": not has_next,
            "data": serialized_data.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        payload = request.data
        # Serialize
        serialized_data = self.create_serializer(data=payload)
        # Validate
        if not serialized_data.is_valid():
            return Response(
                {"error": serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        # Service
        data, status_code = self.service.create(
            album_id=payload["album_id"],
            album_name=payload["album_name"],
            artist_id=payload["artist_id"],
            artist_name=payload["artist_name"],
            image_url=payload["image_url"],
            user=request.user,
        )
        # Response
        return Response(data, status=status_code)


class CriticsView(BaseView):
    service = CriticService
    retrieve_serializer = CriticSerializer
    create_serializer = CreateCriticSerializer

    def get(self, request):
        user_param = request.query_params.get("user_id")
        artist_param = request.query_params.get("artist_id")
        page_param = request.query_params.get("page")
        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Services (list & paginate)
        objects, range = self.service.list(
            user=user_param, page=page_param, artist_id=artist_param
        )
        page, has_next, start_index, end_index, total_objects = ToolkitService.paginate(
            page_number=page_param, range=range, objects=objects
        )
        # Serialize
        serialized_data = self.retrieve_serializer(page, many=True)
        # Response
        response = {
            "total": total_objects,
            "from": start_index,
            "to": end_index,
            "is_last_page": not has_next,
            "data": serialized_data.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        payload = request.data
        # Serialize
        serialized_data = self.create_serializer(data=payload)
        # Validate
        if not serialized_data.is_valid():
            return Response(
                {"error": serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        # Service
        data, status_code = self.service.create(
            album_id=payload["album_id"],
            album_name=payload["album_name"],
            artist_id=payload["artist_id"],
            artist_name=payload["artist_name"],
            content=payload["content"],
            image_url=payload["image_url"],
            user=request.user,
        )
        # Response
        return Response(data, status=status_code)


class VotesView(BaseView):
    service = VoteService
    retrieve_serializer = VoteSerializer
    create_serializer = CreateVoteSerializer

    def get(self, request):
        user_param = request.query_params.get("user_id")
        page_param = request.query_params.get("page")
        stars_param = request.query_params.get("stars")
        artist_param = request.query_params.get("artist_id")

        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Services (list & paginate)
        objects, range = self.service.list(
            user=user_param, page=page_param, artist_id=artist_param, stars=stars_param
        )
        page, has_next, start_index, end_index, total_objects = ToolkitService.paginate(
            page_number=page_param, range=range, objects=objects
        )
        # Serialize
        serialized_data = self.retrieve_serializer(page, many=True)
        # Response
        response = {
            "total": total_objects,
            "from": start_index,
            "to": end_index,
            "is_last_page": not has_next,
            "data": serialized_data.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        payload = request.data
        # Serialize
        serialized_data = self.create_serializer(data=payload)
        # Validate
        if not serialized_data.is_valid():
            return Response(
                {"error": serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        # Enum check
        isCorrectValue = VoteService.check_enum_value(value=float(payload.get("value")))
        if not isCorrectValue:
            return Response(
                {
                    "error": "Value must be in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Service
        data, status_code = self.service.create(
            album_id=payload["album_id"],
            album_name=payload["album_name"],
            artist_id=payload["artist_id"],
            artist_name=payload["artist_name"],
            value=payload["value"],
            image_url=payload["image_url"],
            user=request.user,
        )
        # Response
        return Response(data, status=status_code)


class PlaylistsView(BaseView):
    service = PlaylistService
    retrieve_serializer = PlaylistSerializer
    create_serializer = CreatePlaylistSerializer

    def get(self, request):
        user_param = request.query_params.get("user_id")
        page_param = request.query_params.get("page")
        # Sanity check
        if user_param:
            try:
                int(user_param)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # Services (list & paginate)
        objects, range = self.service.list(user=user_param, page=page_param)
        page, has_next, start_index, end_index, total_objects = ToolkitService.paginate(
            page_number=page_param, range=range, objects=objects
        )
        # Serialize
        serialized_data = self.retrieve_serializer(page, many=True)
        # Response
        response = {
            "total": total_objects,
            "from": start_index,
            "to": end_index,
            "is_last_page": not has_next,
            "data": serialized_data.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        payload = request.data
        # Serialize
        serialized_data = self.create_serializer(data=payload)
        # Validate
        if not serialized_data.is_valid():
            return Response(
                {"error": serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        # Service
        data, status_code = self.service.create(
            album_id=payload["album_id"],
            album_name=payload["album_name"],
            artist_id=payload["artist_id"],
            artist_name=payload["artist_name"],
            image_url=payload["image_url"],
            user=request.user,
        )
        # Response
        return Response(data, status=status_code)
