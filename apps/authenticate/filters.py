from django_filters import rest_framework as filters
from .models import CustomUser

class UserFilter(filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['role']