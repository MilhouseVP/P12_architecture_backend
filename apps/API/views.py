from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import Customer, Contract
from rest_framework.permissions import IsAuthenticated
import P12_backend.permissions as perms
import logging

logger = logging.getLogger('django_file')


class ApiViewsetMixin:
    # logger.warning()
    serializer_actions = ['retrieve', 'update', 'partial_update']

    read_actions = ['list', 'retrieve']
    edit_actions = ['update', 'partial_update']

    serializer_class = None
    create_serializer_class = None
    detail_serializer_class = None

    permission_classes = [IsAuthenticated]
    edit_permissions = [IsAuthenticated, perms.IsSaleReferee]
    create_permissions = [IsAuthenticated, perms.IsSales]
    delete_permissions = [IsAuthenticated, perms.IsManager]

    def get_serializer_class(self):
        if self.action in self.serializer_actions:
            return self.detail_serializer_class
        elif self.action == 'create':
            return self.create_serializer_class
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in self.edit_actions:
            self.permission_classes = self.edit_permissions
        elif self.action =='create':
            self.permission_classes = self.create_permissions
        elif self.action == 'destroy':
            self.permission_classes = self.delete_permissions
        return super().get_permissions()


class CustomersViewset(ApiViewsetMixin, ModelViewSet):
    serializer_class = ListCustomersSerializer
    create_serializer_class = CreateCustomerSerializer
    detail_serializer_class = DetailCustomersSerializer

    def get_queryset(self):
        return Customer.objects.all()


class ContractViewset(ApiViewsetMixin, ModelViewSet):
    serializer_class = ListContractSerializer
    create_serializer_class = CreateContractSerializer
    detail_serializer_class = DetailContractSerializer

    def get_queryset(self):
        return Contract.objects.all()


class EventViewset(ApiViewsetMixin, ModelViewSet):
    serializer_class = ListEventSerializer
    create_serializer_class = CreateEventSerializer
    detail_serializer_class = DetailEventSerializer

    edit_permissions = [IsAuthenticated, perms.IsSupportReferee]
    create_permissions = [IsAuthenticated, perms.IsSales]

    def get_queryset(self):
        return Event.objects.all()
