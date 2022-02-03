from rest_framework.serializers import ModelSerializer
from apps.API.models import Customer
from rest_framework.validators import UniqueTogetherValidator


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone',
            'mobile',
            'email',
            'company',
            'date_created',
            'date_updated'
        )

        validators = [
            UniqueTogetherValidator(queryset=Customer.objects.all(),
                                    fields=['email'],
                                    message= 'email already associated with '
                                             'an existing customer'
                            )
        ]