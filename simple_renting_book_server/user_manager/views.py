from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from user_manager.models import Profile

from user_manager.serializers import (
    LoginSerializer,
    ProfileSerializer,
    RegistrationSerializer,
)


auth_responses = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "token": openapi.Schema(type=openapi.TYPE_STRING, read_only=True),
        },
    )
}


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses=auth_responses)
    @action(methods=["POST"], detail=False, serializer_class=RegistrationSerializer)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _user, token = serializer.save()
        return Response({"token": token}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses=auth_responses)
    @action(methods=["POST"], detail=False, serializer_class=LoginSerializer)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _user, token = serializer.save()
        return Response({"token": token}, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    @action(methods=["GET", "PUT"], detail=False, serializer_class=ProfileSerializer)
    def me(self, request):
        """
        Get or update the request user's profile
        ---
        """
        if request.method == "PUT":
            serializer = self.get_serializer(
                request.user.get_profile(),
                data=request.data,
                context={"user": request.user},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(request.user.get_profile())
            return_data = serializer.data
            # if profile does not exists then set some fields manually
            if return_data["email"] == "":
                return_data["email"] = request.user.email
                return_data["is_staff"] = request.user.is_staff

            return Response(return_data, status=status.HTTP_200_OK)
