from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
from apps.API.models import Customer, Contract, Event
from apps.authenticate.serializers import ListCustomUserSerializer, \
    DetailCustomUserSerializer


class SaleMixin:
    def get_sale_contact(self, instance):
        sale = instance.sale_contact
        serializer = DetailCustomUserSerializer(sale)
        return serializer.data


class ListSaleMixin:
    def get_sale_contact(self, instance):
        sale = instance.sale_contact
        serializer = ListCustomUserSerializer(sale)
        return serializer.data


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
    # TODO: save user id as sale contact
    # def create(self, instance):
    #     pass


class ListCustomersSerializer(ListSaleMixin, ModelSerializer):
    sale_contact = SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'company', 'first_name', 'last_name', 'sale_contact')


class DetailCustomersSerializer(SaleMixin, ModelSerializer):
    sale_contact = SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'


class CreateContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ('sale_contact', 'client', 'amount', 'payement_due')


class ListContractSerializer(ListSaleMixin, ModelSerializer):
    sale_contact = SerializerMethodField()

    class Meta:
        model = Contract
        fields = ('id', 'client', 'status', 'sale_contact')


class DetailContractSerializer(SaleMixin, ModelSerializer):
    sale_contact = SerializerMethodField()

    class Meta:
        model = Contract
        fields = '__all__'

