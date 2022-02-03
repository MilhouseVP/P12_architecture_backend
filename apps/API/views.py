from rest_framework.viewsets import ModelViewSet
from .serializers import CustomerSerializer
from .models import Customer


class CustomersViewset(ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.all()