from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import Customer, Contract


class SerializerMixin:
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        elif self.action == 'create':
            return self.create_serializer_class
        return super().get_serializer_class()


class CustomersViewset(SerializerMixin, ModelViewSet):
    serializer_class = ListCustomersSerializer
    create_serializer_class = CreateCustomerSerializer
    detail_serializer_class = DetailCustomersSerializer

    def get_queryset(self):
        return Customer.objects.all()


class ContractViewset(SerializerMixin, ModelViewSet):
    serializer_class = ListContractSerializer
    create_serializer_clase = CreateContractSerializer
    detail_serializer_class = DetailContractSerializer

    def get_queryset(self):
        return Contract.objects.all()

