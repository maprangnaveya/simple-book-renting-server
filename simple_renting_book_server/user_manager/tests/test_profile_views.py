from django.utils import timezone
from rest_framework.reverse import reverse

from simple_renting_book_server.base_tests import BaseAPITestCase


class ProfileViewTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()

        self.normal_user = self.given_a_new_user()

    def given_a_me_url(self):
        self.given_a_request_url(reverse("v1:profile-me"))

    def given_a_default_normal_user_profile(self):
        self.birth_date = timezone.make_aware(
            timezone.datetime(day=27, month=2, year=1996)
        ).date()
        self.first_name = "Normal"
        self.last_name = "User"
        self.normal_user_profile = self.given_a_new_user_profile(
            user=self.normal_user,
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date,
        )
        return self.normal_user_profile

    def assertKeysInProfileResponse(self):
        self.assertIn("first_name", self.response_json)
        self.assertIn("last_name", self.response_json)
        self.assertIn("email", self.response_json)
        self.assertIn("is_staff", self.response_json)
        self.assertIn("birth_date", self.response_json)

    def test_get_profile_success(self):
        self.given_a_default_normal_user_profile()

        self.given_logged_in_user(self.normal_user)
        self.given_a_me_url()
        self.when_user_get_json()

        self.assertResponseSuccess()
        self.assertKeysInProfileResponse()
        self.assertEqual(self.first_name, self.response_json["first_name"])
        self.assertEqual(self.last_name, self.response_json["last_name"])
        self.assertEqual(self.birth_date.isoformat(), self.response_json["birth_date"])
        self.assertEqual(self.normal_user.email, self.response_json["email"])

    def test_get_profile_sucess_with_null_birth_date(self):
        self.normal_user_profile = self.given_a_default_normal_user_profile()
        self.normal_user_profile.birth_date = None
        self.normal_user_profile.save()

        self.given_logged_in_user(self.normal_user)
        self.given_a_me_url()
        self.when_user_get_json()

        self.assertResponseSuccess()
        self.assertKeysInProfileResponse()
        self.assertEqual(self.first_name, self.response_json["first_name"])
        self.assertEqual(self.last_name, self.response_json["last_name"])
        self.assertEqual(self.normal_user.email, self.response_json["email"])
        self.assertIsNone(self.response_json["birth_date"])

    def test_get_profile_sucess_with_empty_profile(self):
        self.given_logged_in_user(self.normal_user)
        self.given_a_me_url()
        self.when_user_get_json()

        self.assertResponseSuccess()
        self.assertKeysInProfileResponse()
        self.assertEqual(self.normal_user.email, self.response_json["email"])
        self.assertEqual("", self.response_json["first_name"])
        self.assertEqual("", self.response_json["last_name"])
        self.assertIsNone(self.response_json["birth_date"])

    def test_get_profile_failed_with_not_logged_in_user(self):
        self.given_a_me_url()
        self.when_user_get_json()

        self.assertResponseNotAuthorized()

    def test_update_profile_success(self):
        normal_user_profile = self.given_a_default_normal_user_profile()

        self.given_logged_in_user(self.normal_user)
        self.given_a_me_url()

        data = {
            "email": "new_email@mockup.test",
            "first_name": "Brad",
            "last_name": "Dal",
            "birth_date": "1990-01-01",
        }
        self.when_user_put_and_get_json(data)

        self.assertResponseSuccess()
        self.assertKeysInProfileResponse()

        self.assertEqual(data["email"], self.response_json["email"])
        self.assertEqual(data["first_name"], self.response_json["first_name"])
        self.assertEqual(data["last_name"], self.response_json["last_name"])
        self.assertEqual(data["birth_date"], self.response_json["birth_date"])

        normal_user_profile.refresh_from_db()
        self.assertEqual(data["email"], normal_user_profile.user.email)
        self.assertEqual(data["first_name"], normal_user_profile.first_name)
        self.assertEqual(data["last_name"], normal_user_profile.last_name)
        self.assertEqual(data["birth_date"], normal_user_profile.birth_date.isoformat())

    def test_update_profile_failed_with_not_logged_in_user(self):
        self.given_a_me_url()
        self.when_user_put_and_get_json(data={})

        self.assertResponseNotAuthorized()

    def test_update_profile_failed_with_duplicated_new_email(self):
        other_user = self.given_a_new_user(email="other_email@mockup.test")
        normal_user_profile = self.given_a_default_normal_user_profile()

        self.given_logged_in_user(self.normal_user)
        self.given_a_me_url()

        data = {
            "email": other_user.email,
            "first_name": "Brad",
            "last_name": "Dal",
            "birth_date": "1990-01-01",
        }
        self.when_user_put_and_get_json(data)

        self.assertResponseBadRequest()
        self.assertEqual(
            {
                "non_field_errors": [
                    "This email is already being used for another account."
                ]
            },
            self.response_json,
        )

        normal_user_profile.refresh_from_db()
        self.assertNotEqual(data["email"], normal_user_profile.user.email)
        self.assertNotEqual(data["first_name"], normal_user_profile.first_name)
        self.assertNotEqual(data["last_name"], normal_user_profile.last_name)
        self.assertNotEqual(data["birth_date"], normal_user_profile.birth_date)
