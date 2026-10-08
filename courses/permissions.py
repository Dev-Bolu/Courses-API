from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOrAuthenticatedReadOnly(BasePermission):
    """Authenticated users can read. Only staff can create, update or delete."""

    # Shown to logged-in non-staff users who attempt a write.
    message = "Only staff members can create, update or delete this resource."

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return request.method in SAFE_METHODS or user.is_staff