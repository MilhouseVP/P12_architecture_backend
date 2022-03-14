from rest_framework.permissions import BasePermission
from apps.authenticate.models import CustomUser


class GroupMixin:
    def get_group_list(self, user):
        group_list = []
        for group in user.groups.all():
            group_list.append(group.name)
        return group_list

class IsManager(BasePermission, GroupMixin):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        if 'manager' in self.get_group_list(user):
            return True
        else:
            return False


class IsSales(BasePermission, GroupMixin):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        perms = self.get_group_list(user)
        if 'sales' in perms or 'manager' in perms:
            return True
        else:
            return False


class IsSupport(BasePermission, GroupMixin):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        perms = self.get_group_list(user)
        if 'support' in perms or 'manager' in perms:
            return True
        else:
            return False


class IsSaleReferee(BasePermission, GroupMixin):
    def has_object_permission(self, request, view, obj):
        if obj.sale_contact == request.user \
                or 'manager' in self.get_group_list(request.user):
            return True
        else:
            return False


class IsSupportReferee(BasePermission, GroupMixin):
    def has_object_permission(self, request, view, obj):
        if obj.support_contact == request.user \
                or 'manager' in self.get_group_list(request.user):
            return True
        else:
            return False
