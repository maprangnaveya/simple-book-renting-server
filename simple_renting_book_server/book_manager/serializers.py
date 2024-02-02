from rest_framework import serializers

from book_manager.models import Book


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Book
        fields = (
            "isbn",
            "title",
            "authors",
            "published_at",
            "total_in_store",
            "created_at",
        )
