from django import forms
from apps.authenticate.models import CustomUser


class CustomerForm(forms.Form):
    def __init__(self, sales, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sales_choices = []
        for employee in sales:
            id = int(employee['id'])
            mail = employee['email']
            user_data = (id, mail)
            self.sales_choices.append(user_data)
        self.fields['sale_contact'] = forms.ChoiceField(
            choices=self.sales_choices)

    sale_contact = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='sales'))
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    mobile = forms.CharField(max_length=20)
    email = forms.EmailField()
    company = forms.CharField(max_length=100)


class CustomerEditForm(forms.Form):
    def __init__(self, sales, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sales_choices = []
        for employee in sales:
            id = int(employee['id'])
            mail = employee['email']
            user_data = (id, mail)
            self.sales_choices.append(user_data)
        self.fields['sale_contact'] = forms.ChoiceField(
            choices=self.sales_choices)

    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    mobile = forms.CharField(max_length=20)
    email = forms.EmailField()
    company = forms.CharField(max_length=100)
    existing = forms.BooleanField(label='Déjà client', required=False)


class ContractForm(forms.Form):
    def __init__(self, sales, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sales_choices = []
        for employee in sales:
            id = int(employee['id'])
            mail = employee['email']
            user_data = (id, mail)
            self.sales_choices.append(user_data)
        self.fields['sale_contact'] = forms.ChoiceField(
            choices=self.sales_choices)

    amount = forms.IntegerField(min_value=0)
    payement_due = forms.DateField(label='Date de payement',
                                   widget=forms.DateInput(
                                       attrs={'type': 'date'}))


class ContractEditForm(forms.Form):
    def __init__(self, sales, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sales_choices = []
        for employee in sales:
            id = int(employee['id'])
            mail = employee['email']
            user_data = (id, mail)
            self.sales_choices.append(user_data)
        self.fields['sale_contact'] = forms.ChoiceField(
            choices=self.sales_choices)

    amount = forms.IntegerField(min_value=0)
    payement_due = forms.DateField(label='Date de payement',
                                   widget=forms.DateInput(
                                       attrs={'type': 'date'}))
    status = forms.BooleanField(label='contrat en cours', required=False)


class EventForm(forms.Form):
    def __init__(self, support, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support_choices = []
        for employee in support:
            id = int(employee['id'])
            mail = employee['email']
            user_data = (id, mail)
            self.support_choices.append(user_data)
        self.fields['support_contact'] = forms.ChoiceField(
            choices=self.support_choices)

    attendees = forms.IntegerField(min_value=0, label='Jauge')
    event_date = forms.DateTimeField(label='Date', widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}))
    note = forms.CharField(max_length=1024, label='Note')


class EventEditForm(forms.Form):
    def __init__(self, support, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support_choices = []
        for employee in support:
            id = int(employee['id'])
            mail = employee['email']
            user_data = (id, mail)
            self.support_choices.append(user_data)
        self.fields['support_contact'] = forms.ChoiceField(
            choices=self.support_choices)

    attendees = forms.IntegerField(min_value=0, label='Jauge')
    event_date = forms.DateTimeField(label='Date', widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}))
    note = forms.CharField(max_length=1024, label='Note')
    event_status = forms.BooleanField(label='status', required=False)


class UserForm(forms.Form):
    MANAGER = 'manager'
    SALES = 'sales'
    SUPPORT = 'support'

    ROLE_LIST = (
        (MANAGER, 'manager'),
        (SALES, 'sales'),
        (SUPPORT, 'support')
    )
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput)
    phone = forms.CharField()
    mobile = forms.CharField(required=False)
    role = forms.ChoiceField(choices=ROLE_LIST)


class UserEditForm(forms.Form):
    MANAGER = 'manager'
    SALES = 'sales'
    SUPPORT = 'support'

    ROLE_LIST = (
        (MANAGER, 'manager'),
        (SALES, 'sales'),
        (SUPPORT, 'support')
    )
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone = forms.CharField()
    mobile = forms.CharField(required=False)
    role = forms.ChoiceField(choices=ROLE_LIST)


class UserPasswordForm(forms.Form):
    old_password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    new_password = forms.CharField(min_length=8, widget=forms.PasswordInput)
