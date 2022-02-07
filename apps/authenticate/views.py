from rest_framework.generics import CreateAPIView
from .serializers import RegistrationSerializer, DetailCustomUserSerializer
from apps.authenticate.models import CustomUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
import P12_backend.permissions as perms


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer


class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, perms.IsManager]
    serializer_class =  DetailCustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()