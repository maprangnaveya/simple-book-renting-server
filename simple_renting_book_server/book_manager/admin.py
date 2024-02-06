from django.contrib import admin
from django.contrib.postgres.aggregates import StringAgg
from import_export.admin import ImportExportModelAdmin

from simple_renting_book_server.helpers import get_all_field_names, image_tag_thumbnail
from simple_renting_book_server.mixins import EagerLoadingAdminChangeListMixin

from .models import Author, Book


@admin.register(Author)
class AuthorAdminView(ImportExportModelAdmin):
    model = Author
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# TODO: Add button to sync books from openlibrary API
@admin.register(Book)
class BookAdminView(EagerLoadingAdminChangeListMixin, ImportExportModelAdmin):
    model = Book
    fields = (
        "id",
        "isbn",
        "title",
        "total_in_store",
        "authors",
        "image",
        "image_tag",
    )
    readonly_fields = (
        "id",
        "image_tag",
        "created_at",
    )
    list_display = (
        "id",
        "isbn",
        "title",
        "total_in_store",
        "author_names",
    )
    search_fields = (
        "id",
        "title",
        "authors",
    )
    autocomplete_fields = ("authors",)

    def setup_eager_loading(self, queryset):
        return queryset.annotate(
            author_names=StringAgg(
                "authors__name", delimiter=", ", ordering="authors__name"
            ),
        )

    def author_names(self, book) -> str:
        return book.author_names

    def image_tag(self, book) -> str:
        return image_tag_thumbnail(book.image)
