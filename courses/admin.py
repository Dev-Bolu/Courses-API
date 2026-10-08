from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Course, User

admin.site.register(User, UserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "instructor", "price"]
    list_filter = ["category"]
    search_fields = ["title", "instructor"]
    list_select_related = ["category"]