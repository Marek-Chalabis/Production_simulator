from rest_framework import permissions


class AuthorOrAdminPermission(permissions.BasePermission):
    """only author or admin can modify object"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or \
                obj.author == request.user or \
                request.user.is_staff:
            return True
        else:
            return False
