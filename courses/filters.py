import django_filters

from .models import Category, Course


class CategoryFilter(django_filters.FilterSet):
    """Filter categories by name (partial, case-insensitive) or exact slug."""

    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["slug"]


class CourseFilter(django_filters.FilterSet):
    """Filter courses by title, price range, category, instructor, and slug.

    Sorting is handled by DRF's OrderingFilter in the view.
    """

    title = django_filters.CharFilter(lookup_expr="icontains")  # ?title=python

    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", min_value=0
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", min_value=0
    )

    category_name = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )
    category_slug = django_filters.CharFilter(field_name="category__slug")

    instructor = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Course
        fields = ["slug"]