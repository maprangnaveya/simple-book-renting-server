from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import (
    reset_password_token_created,
    post_password_reset,
)

FRONT_END_URL = getattr(settings, "FRONT_END_URL", "")
DEFAULT_FROM_EMAIL = getattr(settings, "DEFAULT_FROM_EMAIL", "")
WEBSITE_TITLE = getattr(settings, "WEBSITE_TITLE", "")


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    context = {
        "current_user": reset_password_token.user,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            FRONT_END_URL, reset_password_token.key
        ),
    }

    email_html_message = render_to_string("./email/user_reset_password.html", context)
    email_plaintext_message = render_to_string(
        "./email/user_reset_password.txt", context
    )

    msg = EmailMultiAlternatives(
        subject=f"Password Reset for {WEBSITE_TITLE}",
        body=email_plaintext_message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
    # TODO: Setup MailCatcher


@receiver(post_password_reset)
def password_has_been_rest(sender, user, reset_password_token, *args, **kwargs):
    context = {
        "current_user": user,
        "email": user.email,
    }

    email_html_message = render_to_string(
        "./email/user_reset_password_success.html", context
    )
    email_plaintext_message = render_to_string(
        "./email/user_reset_password_success.txt", context
    )

    msg = EmailMultiAlternatives(
        subject=f"Your Password Has Reset for {WEBSITE_TITLE}",
        body=email_plaintext_message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
