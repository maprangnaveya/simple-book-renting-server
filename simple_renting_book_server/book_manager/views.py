from django.db.models import Count, F, Value
from django.db.models.functions import Coalesce
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from book_manager.models import Book
from book_manager.serializers import BookSerializer
from rent_manager.models import RentalStatus
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

    @action(methods=["GET"], detail=False)
    def available(self, request):
        queryset = (
            self.filter_queryset(self.get_queryset())
            .annotate(
                books_rented=Coalesce(
                    Count(
                        "rental_logs",
                        filter=F("rental_logs__status") == RentalStatus.ON_GOING,
                    ),
                    Value(0),
                )
            )
            .filter(total_in_store__gt=F("books_rented"))
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
