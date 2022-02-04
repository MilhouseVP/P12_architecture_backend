from rest_framework.permissions import BasePermission
from apps.authenticate.models import CustomUser


# TODO: essayer de faire un mixin
# class PermissionMixin:
#     pass


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        if user.role == 'manager':
            return True
        return False


class IsSales(BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        if user.role == 'sales' or user.role == 'manager':
            return True
        else:
            return False


class IsSupport(BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        if user.role == 'support' or user.role == 'manager':
            return True
        else:
            return False


class IsSaleReferee(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.sale_contact == request.user or request.user.role == 'manager':
            return True
        else:
            return False


class IsSupportReferee(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.support_contact == request.user \
                or request.user.role == 'manager':
            return True
        else:
            return False
