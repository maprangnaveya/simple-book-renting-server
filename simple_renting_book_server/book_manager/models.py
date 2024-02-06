import os

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    def _image_path(instance, filename):
        _name, extension = os.path.splitext(filename)
        datetime_str = timezone.now().strftime("%y%m%d_%H%M%S%f")

        return f"public/books/cover_{datetime_str}{extension}"

    isbn = models.CharField(
        _("ISBN: The International Standard Book Number"),
        max_length=255,
        blank=True,
        db_index=True,
    )
    title = models.CharField(_("Title"), max_length=255, db_index=True)
    authors = models.ManyToManyField(Author, blank=False, related_name="books")
    published_at = models.DateTimeField(_("Published At"), blank=True, null=True)
    total_in_store = models.PositiveSmallIntegerField(_("Total In Store"), default=0)
    image = models.ImageField(blank=True, null=True, upload_to=_image_path)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title
