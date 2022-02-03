from rest_framework.viewsets import ModelViewSet
from .serializers import CreateCustomerSerializer, ListCustomersSerializer, \
    DetailCustomersSerializer
from .models import Customer


class CustomersViewset(ModelViewSet):
    serializer_class = ListCustomersSerializer
    create_serializer_class = CreateCustomerSerializer
    detail_serializer_class =DetailCustomersSerializer

    def get_queryset(self):
        return Customer.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class
        elif self.action == 'retrieve':
            return self.detail_serializer_class
