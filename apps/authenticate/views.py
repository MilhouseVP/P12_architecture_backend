from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, DetailCustomUserSerializer, \
    ChangePasswordSerializer
from apps.authenticate.models import CustomUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
import P12_backend.permissions as perms
from .filters import UserFilter


class RegisterView(CreateAPIView):
    """
    Viewset for registering users
    """
    # permission_classes = [IsAuthenticated, perms.IsManager]
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer


class UserViewset(ModelViewSet):
    """
    Viewset for registered users
    """
    permission_classes = [IsAuthenticated]
    edit_permissions = [IsAuthenticated, perms.IsManager]
    serializer_class = DetailCustomUserSerializer
    filterset_class = UserFilter

    def get_permissions(self):
        """
        permissions selection logic
        :return: Booelans for each permissions in selected permission_classes
        """
        if self.action not in ['list', 'retrieve'] :
            self.permission_classes = self.edit_permissions
        return super().get_permissions()

    def get_queryset(self):
        return CustomUser.objects.filter(is_superuser=False)


class UpdatePassword(ModelViewSet):
    """
    Viewset for users to change their password
    """
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
