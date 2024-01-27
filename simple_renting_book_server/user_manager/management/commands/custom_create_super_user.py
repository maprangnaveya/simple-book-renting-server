from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "dev@mockupemail.com"
        password = settings.SUPER_USER_PASS

        if User.objects.filter(email__iexact=email).exists():
            u = User.objects.get(email__iexact=email)
            u.set_password(password)
            u.is_superuser = True
            u.is_active = True
            u.save()
            self.stdout.write(
                "The superuser account already exists. Password has been reset."
            )
        else:
            u = User.objects.create_superuser(email, password)
            u.is_active = True
            u.save()
            self.stdout.write("The superuser account has been created.")
