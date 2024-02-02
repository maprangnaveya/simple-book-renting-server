from django.contrib.auth import get_user_model, authenticate, password_validation
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user_manager.models import Profile


User = get_user_model()


def custom_validation_error(msg):
    return serializers.ValidationError({"non_field_errors": [msg]})


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    @staticmethod
    def validate_email(value):
        if User.objects.filter(email__iexact=value).exists():
            raise custom_validation_error("This email is already registered.")
        return value.lower()

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.pop("confirm_password")

        password_validation.validate_password(password, self.instance)

        if not password or not confirm_password:
            raise custom_validation_error(
                "Please enter a password and confirm password."
            )

        if password != confirm_password:
            raise custom_validation_error("Passwords do not match.")

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get("email"), password=validated_data.get("password")
        )
        token, _ = Token.objects.get_or_create(user=user)
        return user, token.key

    def update(self, instance, validated_date):
        pass


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            try:
                user = User.objects.get(email__iexact=email)
                if not user.is_active:
                    raise custom_validation_error("This user is inactive.")
            except User.DoesNotExist:
                raise custom_validation_error("This email does not exist.")
        else:
            raise custom_validation_error("Email and password are required.")

        return data

    def create(self, validated_data):
        user = authenticate(
            email=validated_data["email"], password=validated_data["password"]
        )
        if not user:
            raise custom_validation_error("Password is incorrect.")

        token, _ = Token.objects.get_or_create(user=user)
        return user, token.key

    def update(self, instance, validated_date):
        pass


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", required=False)
    is_admin = serializers.BooleanField(source="user.is_staff", read_only=True)

    class Meta:
        model = Profile
        exclude = ("user",)

    def update_email_for_user(self, user, email):
        if user.email.casefold() != email.casefold():
            if User.objects.filter(email__iexact=email).exists():
                raise custom_validation_error(
                    "This email is already being used for another account."
                )
        user.email = email
        user.save()

    def create(self, validated_data):
        is_email_set = False
        user_data = validated_data.pop("user", None)
        if user_data:
            is_email_set = True

        new_profile = validated_data
        new_profile["user"] = self.context["user"]

        if is_email_set:
            self.update_email_for_user(self.context["user"], user_data["email"])
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user
        self.update_email_for_user(user, user_data["email"])

        instance = super().update(instance, validated_data)
        return instance
