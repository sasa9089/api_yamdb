from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Для авторизованных пользователей имеющих статус автора,
     администратора или модератора, иначе только просмотр."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAuthorizedOrAdminOrSuperuser(permissions.BasePermission):
    """Для авторизованных пользователей имеющих статус
    администратора или суперюзера."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAdminOrReadOnly(permissions.BasePermission):
    """Для авторизованных пользователей имеющих статус
    администратора, иначе только просмотр."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
