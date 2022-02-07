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

    def create(self, validated_data ):
        if not 'mobile' in validated_data:
            validated_data['mobile'] = None
        user = self.context['request'].user
        validated_data['sale_contact'] = user
        return Customer.objects.create(**validated_data)


class ListCustomersSerializer(ListSaleMixin, ModelSerializer):
    sale_contact = SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'id', 'company', 'first_name', 'last_name', 'sale_contact',
            'existing')


class DetailCustomersSerializer(SaleMixin, ModelSerializer):
    sale_contact = SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'


class CreateContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ('client', 'amount', 'payement_due')

    def create(self, validated_data ):
        print(validated_data)
        user = self.context['request'].user
        # client = Customer.objects.get(id=validated_data['client'])
        validated_data['sale_contact'] = user
        # validated_data['client'] = client.id
        return Contract.objects.create(**validated_data)


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


class CreateEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('customer', 'support_contact', 'event_status', 'attendees',
                  'event_date', 'note')


class ListEventSerializer(ModelSerializer):
    support_contact = SerializerMethodField()

    class Meta:
        model = Event
        fields = (
        'id', 'event_status', 'support_contact', 'event_date', 'attendees')

    def get_support_contact(self, instance):
        support = instance.support_contact
        serializer = ListCustomUserSerializer(support)
        return serializer.data


class DetailEventSerializer(ModelSerializer):
    support_contact = SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_support_contact(self, instance):
        support = instance.support_contact
        serializer = DetailCustomUserSerializer(support)
        return serializer.data
