from rest_framework.serializers import ModelSerializer
from apps.API.models import Customer
from rest_framework.validators import UniqueTogetherValidator


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_came', 'phone', 'email', 'company')
        # validators = [
        #     UniqueTogetherValidator(queryset=Customer.objects.all(),
        #                             fields=['email'],
        #                             message= 'email already associated with '
        #                                      'an existing customer'
        #                     )
        # ]