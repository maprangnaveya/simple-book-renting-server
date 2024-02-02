from rest_framework.reverse import reverse

from simple_renting_book_server.base_tests import BaseAPITestCase


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
