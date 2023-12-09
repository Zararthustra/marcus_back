from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from .services import CriticService, MasterpieceService, VoteService, PlaylistService


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class MusicVoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.service = VoteService()
        self.url = reverse("music_votes")
        self.token = "Bearer {}".format(get_tokens_for_user(self.user).get("access"))

    def test_vote_views(self):
        # Create
        response = self.client.post(self.url, {
            "album_id": "1",
            "album_name": "album name",
            "value": "4",
            "artist_id": "1",
            "artist_name": "artist name",
            "image_url": "https://url.com",
        },
        HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)

        # Retrieve
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('total'), 1)

        # Delete
        vote_id = response.json().get('data')[0]["id"]
        response = self.client.delete(self.url + "?id=" + vote_id,
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(response.status_code, 204)

    def test_vote_service(self):
        # create()
        _, status_code = self.service.create(
            user=self.user,
            album_id="1",
            album_name="album name",
            value="3.5",
            artist_id="1",
            artist_name="artist name",
            image_url="http://url.com",
        )
        self.assertEqual(status_code, 201)
        _, status_code = self.service.create(
            user=self.user,
            album_id="1",
            album_name="album name",
            value="3.5",
            artist_id="1",
            artist_name="artist name",
            image_url="http://url.com",
        )
        self.assertEqual(status_code, 400)

        # list()
        list, _ = self.service.list(user=self.user, artist_id=None, page=None, stars=3)
        self.assertEqual(len(list), 0)
        list, _ = self.service.list(user=self.user, artist_id=None, page=None, stars=3.5)
        self.assertEqual(len(list), 1)

        # delete()
        vote_id = list[0].id
        status_code = self.service.delete(user=self.user, id=vote_id)
        self.assertEqual(status_code, 204)


class MusicCriticTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.service = CriticService()
        self.url = reverse("music_critics")
        self.token = "Bearer {}".format(get_tokens_for_user(self.user).get("access"))

    def test_critic_views(self):
        # Create
        response = self.client.post(self.url, {
            "album_id": "1",
            "album_name": "album name",
            "content": "my critic",
            "artist_id": "1",
            "artist_name": "artist name",
            "image_url": "https://url.com",
        },
        HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)

        # Retrieve
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('total'), 1)

        # Delete
        vote_id = response.json().get('data')[0]["id"]
        response = self.client.delete(self.url + "?id=" + vote_id,
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(response.status_code, 204)

    def test_critic_service(self):
        # create()
        _, status_code = self.service.create(
            user=self.user,
            album_id="1",
            album_name="album name",
            content="my critic",
            artist_id="1",
            artist_name="artist name",
            image_url="http://url.com",
        )
        self.assertEqual(status_code, 201)
        _, status_code = self.service.create(
            user=self.user,
            album_id="1",
            album_name="album name",
            content="my critic",
            artist_id="1",
            artist_name="artist name",
            image_url="http://url.com",
        )
        self.assertEqual(status_code, 400)

        # list()
        list, _ = self.service.list(artist_id="23", page=None, user=None)
        self.assertEqual(len(list), 0)
        list, _ = self.service.list(artist_id="1", page=None, user=None)
        self.assertEqual(len(list), 1)

        # delete()
        vote_id = list[0].id
        status_code = self.service.delete(user=self.user, id=vote_id)
        self.assertEqual(status_code, 204)


# class MovieWatchlistTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser")
#         self.service = WatchlistService()
#         self.url = reverse("watchlists")
#         self.token = "Bearer {}".format(get_tokens_for_user(self.user).get("access"))

#     def test_watchlist_views(self):
#         # Create
#         response = self.client.post(self.url, {
#             "movie_id": "872585",
#             "movie_name": "movie name",
#             "platform": "movie"
#         },
#         HTTP_AUTHORIZATION=self.token)
#         self.assertEqual(response.status_code, 201)

#         # Retrieve
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json().get('total'), 1)

#         # Delete
#         response = self.client.delete(self.url + "?movie_id=872585",
#             HTTP_AUTHORIZATION=self.token
#         )
#         self.assertEqual(response.status_code, 204)

#     def test_watchlist_service(self):
#         # create()
#         _, status_code = self.service.create(
#             user=self.user,
#             movie_id="872585",
#             movie_name="movie name",
#             platform="movie"
#         )
#         self.assertEqual(status_code, 201)
#         _, status_code = self.service.create(
#             user=self.user,
#             movie_id="872585",
#             movie_name="movie name",
#             platform="movie"
#         )
#         self.assertEqual(status_code, 400)

#         # list()
#         list, _ = self.service.list(user=self.user, page=None)
#         self.assertEqual(len(list), 1)

#         # delete()
#         status_code = self.service.delete(user=self.user, movie_id="872585")
#         self.assertEqual(status_code, 204)


# class MovieMasterpieceTest(TestCase):
    # def setUp(self):
    #     self.user = User.objects.create_user(username="testuser")
    #     self.service = MasterpieceService()
    #     self.url = reverse("masterpieces")
    #     self.token = "Bearer {}".format(get_tokens_for_user(self.user).get("access"))

    # def test_masterpiece_views(self):
    #     # Create
    #     response = self.client.post(self.url, {
    #         "movie_id": "872585",
    #         "movie_name": "movie name",
    #         "platform": "movie"
    #     },
    #     HTTP_AUTHORIZATION=self.token)
    #     self.assertEqual(response.status_code, 201)

    #     # Retrieve
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json().get('total'), 1)

    #     # Delete
    #     response = self.client.delete(self.url + "?movie_id=872585",
    #         HTTP_AUTHORIZATION=self.token
    #     )
    #     self.assertEqual(response.status_code, 204)

    # def test_masterpiece_service(self):
    #     # create()
    #     _, status_code = self.service.create(
    #         user=self.user,
    #         movie_id="872585",
    #         movie_name="movie name",
    #         platform="movie"
    #     )
    #     self.assertEqual(status_code, 201)
    #     _, status_code = self.service.create(
    #         user=self.user,
    #         movie_id="872585",
    #         movie_name="movie name",
    #         platform="movie"
    #     )
    #     self.assertEqual(status_code, 400)

    #     # list()
    #     list, _ = self.service.list(user=self.user, page=None)
    #     self.assertEqual(len(list), 1)

    #     # delete()
    #     status_code = self.service.delete(user=self.user, movie_id="872585")
    #     self.assertEqual(status_code, 204)