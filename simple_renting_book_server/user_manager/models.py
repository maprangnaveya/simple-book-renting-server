import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """
    Contains user authentication data and permissions to do with system access
    """

    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_active = models.BooleanField(_("active status"), default=True)

    from user_manager.managers import UserManager

    objects: UserManager = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_staff(self) -> bool:
        """
        Is user has access to django admin
        """
        return self.is_superuser

    def get_profile(self):
        try:
            return Profile.objects.get(user=self)
        except Profile.DoesNotExist:
            return None

    def __str__(self) -> str:
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(_("First name"), blank=False, null=False)
    last_name = models.CharField(_("Last name"), blank=False, null=False)
    birth_date = models.DateField(_("Birthdate"), blank=True, null=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profile")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self) -> str:
        return self.full_name
