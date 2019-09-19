from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit only their own profiles and not others"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id==request.user.id