from rest_framework.permissions import BasePermission
from apps.authenticate.models import CustomUser


class GroupMixin:
    """
    mixin to add a get_group method by inheritance
    """
    def get_group_list(self, user):
        group_list = []
        for group in user.groups.all():
            group_list.append(group.name)
        return group_list

class IsManager(BasePermission, GroupMixin):
    """
    permission that return True if the user is a manager
    """
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        if 'manager' in self.get_group_list(user):
            return True
        else:
            return False


class IsSales(BasePermission, GroupMixin):
    """
    permission that return True if user is sales
    """
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        perms = self.get_group_list(user)
        if 'sales' in perms or 'manager' in perms:
            return True
        else:
            return False


class IsSupport(BasePermission, GroupMixin):
    """
    permission that return True is user is support
    """
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        perms = self.get_group_list(user)
        if 'support' in perms or 'manager' in perms:
            return True
        else:
            return False


class IsSaleReferee(BasePermission, GroupMixin):
    """
    permission that return True if the user is the sale_contact of an object
    """
    def has_object_permission(self, request, view, obj):
        if obj.sale_contact == request.user \
                or 'manager' in self.get_group_list(request.user):
            return True
        else:
            return False


class IsSupportReferee(BasePermission, GroupMixin):
    """
    permission that return True if user is support_contact of an event
    """
    def has_object_permission(self, request, view, obj):
        if obj.support_contact == request.user \
                or 'manager' in self.get_group_list(request.user):
            return True
        else:
            return False
