from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from user_manager.models import Profile


User = get_user_model()


class BaseAPITestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.client_user = None
        self.response = None

    def given_a_new_user(
        self, email="normal_user@mockup.test", password="strongpassword", role=None
    ):
        return User.objects.create_user(email, password=password, role=role)

    def given_a_new_user_profile(
        self, user, first_name="Jane", last_name="Doe", birth_date=None
    ):
        return Profile.objects.create(
            user=user, first_name=first_name, last_name=last_name, birth_date=birth_date
        )

    def given_a_request_url(self, url):
        self.url = url

    def given_logged_in_user(self, user):
        self.client_user = user
        self.client.force_login(user)

    def when_user_get_json(self, format="json"):
        self.response = self.client.get(self.url, format=format)
        self.response_json = self.response.json()

    def when_user_patch_get_get_json(self, data, format="json"):
        self.response = self.client.patch(self.url, data, format=format)
        self.response_json = self.response.json()

    def when_user_post_get_get_json(self, data, format="json"):
        self.response = self.client.post(self.url, data, format=format)
        self.response_json = self.response.json()

    def when_user_put_get_get_json(self, data, format="json"):
        self.response = self.client.put(self.url, data, format=format)
        self.response_json = self.response.json()

    def when_user_delete(self, **kwargs):
        self.response = self.client.delete(self.url, format="json", **kwargs)

    def assertResponseSuccess(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def assertResponseCreated(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def assertResponseSuccessNoContent(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def assertResponseBadRequest(self):
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertResponseNotAuthorized(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertResponseForbidden(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def assertResponseNotFound(self):
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)
