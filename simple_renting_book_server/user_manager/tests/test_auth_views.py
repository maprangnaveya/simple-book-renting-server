from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


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

    def given_a_request_url(self, url):
        self.url = url

    def given_logged_in_user(self, user):
        self.client_user = user
        self.client.force_login(user)

    def when_user_get_json(self, format="json"):
        self.response = self.client.patch(self.url, format=format)
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


class AuthViewTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()

        self.default_email = "new_user@mockup.test"
        self.default_password = "VeryStrongPassword!!"

    def given_a_login_url(self):
        self.given_a_request_url(reverse("v1:auth-login"))

    def given_a_register_url(self):
        self.given_a_request_url(reverse("v1:auth-register"))

    def test_login_success(self):
        _exist_user = self.given_a_new_user(
            email=self.default_email, password=self.default_password
        )

        data = {"email": self.default_email, "password": self.default_password}
        self.given_a_login_url()
        self.when_user_post_get_get_json(data)

        self.assertResponseSuccess()
        self.assertIsNotNone(self.response_json["token"])

    def test_login_failed_with_nonexist_user(self):
        data = {
            "email": "nonexist_user@mockup.test",
            "password": self.default_password,
        }
        self.given_a_login_url()
        self.when_user_post_get_get_json(data)

        self.assertResponseBadRequest()
        self.assertIsNotNone(
            {"non_field_errors": "This email does not exist."}, self.response_json
        )

    def test_login_failed_with_incorrect_password(self):
        data = {"email": self.default_email, "password": "VeryWrongPassword"}
        self.given_a_login_url()
        self.when_user_post_get_get_json(data)

        self.assertResponseBadRequest()
        self.assertIsNotNone(
            {"non_field_errors": "Password is incorrect."}, self.response_json
        )

    def test_login_failed_with_missing_data(self):
        data = {}
        self.given_a_login_url()
        self.when_user_post_get_get_json(data)

        self.assertResponseBadRequest()
        self.assertIsNotNone(
            {"non_field_errors": "Email and password are required."}, self.response_json
        )

    def test_register_success(self):
        data = {
            "email": self.default_email,
            "password": self.default_password,
            "confirm_password": self.default_password,
        }
        self.given_a_register_url()
        self.when_user_post_get_get_json(data)

        self.assertResponseCreated()
        self.assertIsNotNone(self.response_json["token"])

    def test_register_failed_with_existing_email(self):
        exist_user = self.given_a_new_user(email=self.default_email)

        data = {
            "email": exist_user.email,
            "password": self.default_password,
            "confirm_password": self.default_password,
        }
        self.given_a_register_url()
        self.when_user_post_get_get_json(data)

        self.assertResponseBadRequest()
        self.assertIsNotNone(
            {"non_field_errors": "This email is already registered."},
            self.response_json,
        )

    def test_register_failed_with_mismatch_password(self):
        data = {
            "email": self.default_email,
            "password": self.default_password,
            "confirm_password": self.default_password + "-SomeSpecial",
        }
        self.given_a_register_url()
        self.when_user_post_get_get_json(data)

        self.assertResponseBadRequest()
        self.assertIsNotNone(
            {"non_field_errors": "Passwords do not match."}, self.response_json
        )
