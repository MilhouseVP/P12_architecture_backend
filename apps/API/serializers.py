from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
from apps.API.models import Customer
from apps.authenticate.serializers import ListCustomUserSerializer, \
    DetailCustomUserSerializer


class CreateCustomerSerializer(ModelSerializer):
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
            'date_updated',
            'sale_contact'

        )

        validators = [
            UniqueTogetherValidator(queryset=Customer.objects.all(),
                                    fields=['email'],
                                    message='email already associated with '
                                            'an existing customer'
                                    )
        ]


class ListCustomersSerializer(ModelSerializer):
    sale_contact = SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'company', 'first_name', 'last_name', 'sale_contact')

    def get_sale_contact(self, instance):
        sale = instance.sale_contact
        serializer = ListCustomUserSerializer(sale)
        return serializer.data


class DetailCustomersSerializer(ModelSerializer):
    sale_contact = SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    def get_sale_contact(self, instance):
        sale = instance.sale_contact
        serializer = DetailCustomUserSerializer(sale)
        return serializer.data
