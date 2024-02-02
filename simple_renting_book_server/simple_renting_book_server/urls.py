"""
URL configuration for simple_renting_book_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from book_manager.views import BookViewSet
from user_manager.views import AuthViewSet, ProfileViewSet


api_v1 = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API for application",
    ),
)

router_v1 = routers.DefaultRouter()
router_v1.register(r"auth", AuthViewSet, basename="auth")
router_v1.register(r"profile", ProfileViewSet, basename="profile")
router_v1.register(r"books", BookViewSet, basename="books")

urlpatterns = [
    path(
        "api-explorer/",
        api_v1.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/v1/", include((router_v1.urls, "api"), namespace="v1")),
    path(
        "api/v1/auth/password-reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
