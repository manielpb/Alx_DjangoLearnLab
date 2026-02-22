from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Read-only for everyone.
    Write actions only allowed for the object's author.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS for anyone
        if request.method in SAFE_METHODS:
            return True

        # Otherwise only the owner can modify
        return getattr(obj, "author", None) == request.user