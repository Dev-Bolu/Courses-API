from rest_framework import serializers

from .models import Category, Course

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



    
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="course-detail",
        lookup_field="slug",
    )

    class Meta:
        model = Category
        fields = ["url", "id", "name", "slug", "courses"]
        read_only_fields = ["id", "slug"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.HyperlinkedRelatedField(
        view_name="category-detail",
        lookup_field="slug",
        queryset=Category.objects.all(),
    )
    # Free convenience field: the view already uses select_related("category")
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Course
        fields = [
            "url", "id", "title", "slug", "instructor",
            "price", "category", "category_name", "description",
        ]
        read_only_fields = ["id", "slug"]
        extra_kwargs = {"url": {"lookup_field": "slug"}}
        

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Emails are stored lowercase, so normalise the login input too
        attrs[self.username_field] = attrs[self.username_field].strip().lower()
        return super().validate(attrs) 