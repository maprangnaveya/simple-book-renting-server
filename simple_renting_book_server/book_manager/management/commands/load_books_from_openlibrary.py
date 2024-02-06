import requests


from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from ...models import Author, Book

User = get_user_model()


class Command(BaseCommand):

    def request_books(self):
        url = "https://openlibrary.org/search.json?q=sherlock&limit=2"
        response = requests.request(
            "get", url, headers={"content-type": "application/json"}
        )
        return (
            response.json(),
            response.status_code == 200,
        )

    def handle(self, *args, **kwargs):
        book_search_json, is_succcess = self.request_books()
        if not is_succcess:
            raise CommandError("Fail to request books from openlibrary")

        book_results = book_search_json["docs"]
        imported_books = 0

        for book in book_results:
            isbn_list = book.get("isbn")
            isbn = isbn_list[0] if isbn_list else ""

            authors = []
            for author_name in book.get("author_name", []):
                author, _created = Author.objects.get_or_create(name=author_name)
                authors.append(author.id)

            if not authors:
                continue

            book_obj, _ = Book.objects.update_or_create(
                title=book["title"], isbn=isbn, total_in_store=1
            )

            book_obj.authors.add(*authors)
            imported_books += 1

        self.stdout.write(
            self.style.SUCCESS(f"Import {imported_books} books successfully")
        )
