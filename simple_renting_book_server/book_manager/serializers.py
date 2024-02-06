from rest_framework import serializers

from book_manager.models import Book


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    image = serializers.ImageField(read_only=True)
    available_in_store = serializers.SerializerMethodField()

    def get_available_in_store(self, obj):
        # TODO: Get an available in store
        return obj.total_in_store

    class Meta:
        model = Book
        fields = (
            "id",
            "isbn",
            "title",
            "authors",
            "published_at",
            "total_in_store",
            "available_in_store",
            "image",
        )
