from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == UserRoles.MODERATOR
