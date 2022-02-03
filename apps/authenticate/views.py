from rest_framework.generics import CreateAPIView
from .serializers import RegistrationSerializer
from apps.authenticate.models import CustomUser

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer