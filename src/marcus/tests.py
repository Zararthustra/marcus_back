from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from .services import CriticService, MasterpieceService, VoteService, WatchlistService


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.login_url = reverse("token_obtain_pair")
        self.reconnect_url = reverse("token_refresh")
        self.register_url = reverse("register")
        self.user_refresh_token = get_tokens_for_user(self.user).get("refresh")

    def test_create_user(self):
        self.assertEqual(self.user.username, "testuser")

    def test_delete_user(self):
        self.user.delete()
        self.assertEqual(self.user.id, None)

    def test_unauthorized_user(self):
        response = self.client.post("/api/votes", {
            "movie_id": "1",
            "movie_name": "movie name",
            "value": 2.5,
            "platform": "movie"
        })
        self.assertEqual(response.status_code, 401)
    
    def test_login_user(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "password"
        })
        self.assertEqual(response.status_code, 200)
    
    def test_reconnect_user(self):
        response = self.client.post(self.reconnect_url, {
            "refresh": self.user_refresh_token
        })
        self.assertEqual(response.status_code, 200)
    
    def test_register_user(self):
        response = self.client.post(self.register_url , {
            "username": "newuser",
            "password": "password"
        })
        self.assertEqual(response.status_code, 201)


class MovieVoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.service = VoteService()
        self.url = reverse("votes")
        self.token = "Bearer {}".format(get_tokens_for_user(self.user).get("access"))

    def test_vote_views(self):
        # Create
        response = self.client.post(self.url, {
            "movie_id": "1",
            "movie_name": "movie name",
            "value": 2.5,
            "platform": "movie"
        },
        HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)

        # Retrieve
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('total'), 1)

        # Delete
        response = self.client.delete(self.url + "?movie_id=1",
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(response.status_code, 204)

    def test_vote_service(self):
        # check_enum_value()
        value_accepted = self.service.check_enum_value(value=4)
        self.assertEqual(value_accepted, True)
        value_accepted = self.service.check_enum_value(value=9)
        self.assertEqual(value_accepted, False)

        # create()
        _, status_code = self.service.create(
            user=self.user,
            value=4,
            movie_id="1",
            movie_name="movie name",
            platform="movie"
        )
        self.assertEqual(status_code, 201)
        _, status_code = self.service.create(
            user=self.user,
            value=4,
            movie_id="1",
            movie_name="movie name",
            platform="movie"
        )
        self.assertEqual(status_code, 400)

        # list()
        list, _ = self.service.list(user=self.user, stars=3, movie_id="1")
        self.assertEqual(len(list), 0)
        list, _ = self.service.list(user=self.user, stars=4, movie_id="1")
        self.assertEqual(len(list), 1)

        # delete()
        status_code = self.service.delete(user=self.user, movie_id="1")
        self.assertEqual(status_code, 204)


class MovieCriticTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.service = CriticService()
        self.url = reverse("critics")
        self.token = "Bearer {}".format(get_tokens_for_user(self.user).get("access"))

    def test_critic_views(self):
        # Create
        response = self.client.post(self.url, {
            "movie_id": "1",
            "movie_name": "movie name",
            "content": "test critic",
            "platform": "movie"
        },
        HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)

        # Retrieve
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('total'), 1)

        # Delete
        response = self.client.delete(self.url + "?movie_id=1",
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(response.status_code, 204)

    def test_critic_service(self):
        # create()
        _, status_code = self.service.create(
            user=self.user,
            content="test critic",
            movie_id="1",
            movie_name="movie name",
            platform="movie"
        )
        self.assertEqual(status_code, 201)
        _, status_code = self.service.create(
            user=self.user,
            content="test critic",
            movie_id="1",
            movie_name="movie name",
            platform="movie"
        )
        self.assertEqual(status_code, 400)

        # list()
        list, _ = self.service.list(user=self.user)
        self.assertEqual(len(list), 1)

        # list_by_movie_id_and_aggregate_votes()
        list = self.service.list_by_movie_id_and_aggregate_votes(movie="1")
        self.assertEqual(len(list), 1)

        # delete()
        status_code = self.service.delete(user=self.user, movie_id="1")
        self.assertEqual(status_code, 204)


class MovieWatchlistTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.service = WatchlistService()
        self.url = reverse("watchlists")
        self.token = "Bearer {}".format(get_tokens_for_user(self.user).get("access"))

    def test_watchlist_views(self):
        # Create
        response = self.client.post(self.url, {
            "movie_id": "872585",
            "movie_name": "movie name",
            "platform": "movie"
        },
        HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)

        # Retrieve
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('total'), 1)

        # Delete
        response = self.client.delete(self.url + "?movie_id=872585",
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(response.status_code, 204)

    def test_watchlist_service(self):
        # create()
        _, status_code = self.service.create(
            user=self.user,
            movie_id="872585",
            movie_name="movie name",
            platform="movie"
        )
        self.assertEqual(status_code, 201)
        _, status_code = self.service.create(
            user=self.user,
            movie_id="872585",
            movie_name="movie name",
            platform="movie"
        )
        self.assertEqual(status_code, 400)

        # list()
        list, _ = self.service.list(user=self.user, page=None)
        self.assertEqual(len(list), 1)

        # delete()
        status_code = self.service.delete(user=self.user, movie_id="872585")
        self.assertEqual(status_code, 204)


class MovieMasterpieceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.service = MasterpieceService()
        self.url = reverse("masterpieces")
        self.token = "Bearer {}".format(get_tokens_for_user(self.user).get("access"))

    def test_masterpiece_views(self):
        # Create
        response = self.client.post(self.url, {
            "movie_id": "872585",
            "movie_name": "movie name",
            "platform": "movie"
        },
        HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)

        # Retrieve
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('total'), 1)

        # Delete
        response = self.client.delete(self.url + "?movie_id=872585",
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(response.status_code, 204)

    def test_masterpiece_service(self):
        # create()
        _, status_code = self.service.create(
            user=self.user,
            movie_id="872585",
            movie_name="movie name",
            platform="movie"
        )
        self.assertEqual(status_code, 201)
        _, status_code = self.service.create(
            user=self.user,
            movie_id="872585",
            movie_name="movie name",
            platform="movie"
        )
        self.assertEqual(status_code, 400)

        # list()
        list, _ = self.service.list(user=self.user, page=None)
        self.assertEqual(len(list), 1)

        # delete()
        status_code = self.service.delete(user=self.user, movie_id="872585")
        self.assertEqual(status_code, 204)