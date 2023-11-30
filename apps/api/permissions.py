from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff or request.method in SAFE_METHODS)


class IsSuperUserOrIsStaffReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_superuser or
            request.user and request.user.is_staff and request.method in SAFE_METHODS
        )
