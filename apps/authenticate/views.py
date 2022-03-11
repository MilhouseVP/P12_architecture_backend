from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, DetailCustomUserSerializer, \
    ChangePasswordSerializer
from apps.authenticate.models import CustomUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
import P12_backend.permissions as perms


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer


class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, perms.IsManager]
    serializer_class = DetailCustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()


class UpdatePassword(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response({'detail': 'Ancien mot de passe incorrect.'},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(DetailCustomUserSerializer(self.object).data)
        else:
            return Response({'detail': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
