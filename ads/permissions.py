from rest_framework import permissions

from users.models import User


class IsOwnerSelection(permissions.BasePermission):
    message = 'Вы не владелец подборки'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsOwnerAdOrStaff(permissions.BasePermission):
    message = 'Вы не владелец объявления'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user.role in [User.STATUS.admin, User.STATUS.moderator]:
            return True
        return False
