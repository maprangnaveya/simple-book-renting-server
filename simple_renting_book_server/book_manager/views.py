from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from book_manager.models import Book
from book_manager.serializers import BookSerializer
from simple_renting_book_server.mixins import PaginationListViewSetMixin


class BookViewSet(PaginationListViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = BookSerializer
    queryset = Book.objects.prefetch_related("authors")

    filterset_fields = {
        "title": [
            "exact",
            "icontains",
        ],
        "authors__name": [
            "exact",
            "icontains",
        ],
    }
    ordering_fields = ["title"]
    search_fields = ["title", "authors__name"]
