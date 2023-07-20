from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsStaffNotCreateOrDelete(BasePermission):
    message = 'Вы модератор, у вас нет доступа к этому функционалу'

    def has_permission(self, request, view):
        if request.user.is_staff:
            return False
        return True


class IsStaffUpdate(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsOwnerAndStaffList(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить доступ, если пользователь сотрудник (is_staff=True)
        if request.user.is_staff:
            return True

        # Разрешить доступ, если пользователь является владельцем урока (owner)
        return request.user == obj.owner