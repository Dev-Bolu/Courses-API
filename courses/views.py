from django.db.models import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView

from .filters import CategoryFilter, CourseFilter
from .models import Category, Course
from .permissions import IsStaffOrAuthenticatedReadOnly
from .serializers import (
    CategorySerializer,
    CourseSerializer,
    EmailTokenObtainPairSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    # prefetch_related avoids N+1 queries from the `courses` links
    queryset = Category.objects.prefetch_related("courses")
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [IsStaffOrAuthenticatedReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = CategoryFilter
    search_fields = ["name", "slug"]
    ordering_fields = ["name", "id"]
    ordering = ["name"]

    def destroy(self, request, *args, **kwargs):
        # Course.category uses on_delete=PROTECT
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "Cannot delete a category that still has courses."},
                status=status.HTTP_409_CONFLICT,
            )


class CourseViewSet(viewsets.ModelViewSet):
    # select_related fetches Category in the same query (avoids N+1)
    queryset = Course.objects.select_related("category")
    serializer_class = CourseSerializer
    lookup_field = "slug"
    permission_classes = [IsStaffOrAuthenticatedReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = CourseFilter
    search_fields = ["title", "instructor", "description", "category__name"]
    ordering_fields = ["price", "title", "id"]
    ordering = ["title"]


class LoginView(TokenObtainPairView):
    """JWT login: case-insensitive email, limited by the "login" throttle rate."""

    serializer_class = EmailTokenObtainPairSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"