from django.utils import timezone
from rest_framework.reverse import reverse
from book_manager.models import Author, Book

from simple_renting_book_server.base_tests import BaseAPITestCase


class BookViewTestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.normal_user = self.given_a_new_user()

        self.book_rabbit_and_turtle = self.given_a_new_book(
            title="Rabbit and Turtle", isbn="000000000001"
        )
        self.book_cinderella = self.given_a_new_book(
            title="Cinderella", isbn="000000000002"
        )
        self.book_rapunzel = self.given_a_new_book(
            title="Rapunzel", isbn="000000000003"
        )

        self.author_aesop = self.given_a_new_author(name="Aesop")
        self.author_brothers_grimm = self.given_a_new_author(name="Brothers Grimm")

        self.author_aesop.books.add(self.book_rabbit_and_turtle)
        self.author_brothers_grimm.books.add(self.book_cinderella, self.book_rapunzel)

    def given_a_new_book(self, **details):
        return Book.objects.create(**details)

    def given_a_new_author(self, **details):
        return Author.objects.create(**details)

    def given_a_books_url(self):
        self.given_a_request_url(reverse("v1:books-list"))

    def assertKeysInPaginationResponse(self):
        self.assertIn("count", self.response_json)
        self.assertIn("next", self.response_json)
        self.assertIn("previous", self.response_json)
        self.assertIn("results", self.response_json)

    def assertKeysInBookResponse(self, response_json):
        self.assertIn("isbn", response_json)
        self.assertIn("title", response_json)
        self.assertIn("authors", response_json)
        self.assertIn("published_at", response_json)
        self.assertIn("total_in_store", response_json)

    def test_get_books_success(self):
        self.given_logged_in_user(self.normal_user)
        self.given_a_books_url()

        self.when_user_get_json()

        self.assertResponseSuccess()
        self.assertKeysInPaginationResponse()
        response_json = self.response_json["results"][0]
        self.assertKeysInBookResponse(response_json)

        book = Book.objects.order_by("title").first()
        self.assertEqual(book.isbn, response_json["isbn"])
        self.assertEqual(book.title, response_json["title"])
        self.assertEqual(book.published_at, response_json["published_at"])
        self.assertEqual(
            list(book.authors.values_list("name", flat=True)), response_json["authors"]
        )

    def test_get_books_success_without_pagination(self):
        self.given_logged_in_user(self.normal_user)
        self.given_a_books_url()
        self.given_page_query_param(-1)

        self.when_user_get_json()

        self.assertResponseSuccess()
        self.assertNotIn("count", self.response_json)
        self.assertNotIn("next", self.response_json)
        self.assertNotIn("previous", self.response_json)
        self.assertNotIn("results", self.response_json)

        self.assertKeysInBookResponse(self.response_json[0])

    def test_search_books_by_title_success(self):
        pass

    def test_search_books_by_authors_success(self):
        pass

    def test_get_books_succes_when_ordering_title_desc(self):
        pass

    def test_get_books_succes_when_ordering_title_asc(self):
        pass

    def test_get_books_failed_with_invalid_page_0_return_not_found_invalid_page(self):
        self.given_a_books_url()
        self.given_page_query_param(0)

        self.when_user_get_json()

        self.assertResponseNotFound()

    def test_get_books_failed_with_invalid_page_return_not_found_invalid_page(self):
        self.given_a_books_url()
        self.given_page_query_param(10000)

        self.when_user_get_json()

        self.assertResponseNotFound()
        self.assertEqual(self.response_json["detail"], "Invalid page.")
