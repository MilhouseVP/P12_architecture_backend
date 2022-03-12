from django_filters import rest_framework as filters
from .models import *

class ContractFilter(filters.FilterSet):
    class Meta:
        model = Contract
        fields = [
            'customer__email',
            'customer__last_name',
            'date_created',
            'amount',
            'sale_contact'
        ]


class EventFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = [
            'customer__email',
            'customer__last_name',
            'event_date',
            'support_contact'
        ]


class CustomerFilter(filters.FilterSet):
    class Meta:
        model = Customer
        fields = [
            'email',
            'last_name',
            'company'
        ]