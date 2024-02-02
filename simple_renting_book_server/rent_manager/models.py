from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from book_manager.models import Book

User = get_user_model()


class RentalStatus(models.TextChoices):
    ON_GOING = "ON_GOING", "On Going"
    RETURNED = "RETURNED", "Returned"
    OVERDUE = "OVERDUE", "Overdue"


class RentalLog(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="rental_logs")
    rent_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rental_logs"
    )
    rent_date = models.DateTimeField(_("Rent At DateTime"), db_index=True)
    price = models.DecimalField(_("Rent Price"), max_digits=10, decimal_places=2)
    due_date = models.DateField(_("Expected Return Date"))
    return_date = models.DateTimeField(_("Return At DateTime"), blank=True, null=True)
    status = models.CharField(
        _("Reant Status"),
        max_length=8,
        choices=RentalStatus.choices,
        default=RentalStatus.ON_GOING,
    )

    def save(self, *args, **kwargs):
        if self.return_date is not None:
            self.status = RentalStatus.RETURNED
        elif timezone.now() >= self.due_date:
            self.status = RentalStatus.OVERDUE
        else:
            self.status = RentalStatus.ON_GOING

        super().save(*args, **kwargs)
