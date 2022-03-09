from django import forms
from apps.authenticate.models import CustomUser


class CustomerForm(forms.Form):
    sale_contact = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='sales'))
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    mobile = forms.CharField(max_length=20)
    email = forms.EmailField()
    company = forms.CharField(max_length=100)


class CustomerEditForm(forms.Form):
    sale_contact = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='sales'))
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    mobile = forms.CharField(max_length=20)
    email = forms.EmailField()
    company = forms.CharField(max_length=100)
    existing = forms.BooleanField(label='Déjà client', required=False)


class ContractForm(forms.Form):
    amount = forms.IntegerField(min_value=0)
    payement_due = forms.DateField(label='Date de payement',
                                   widget=forms.DateInput(
                                       attrs={'type': 'date'}))


class ContractEditForm(forms.Form):
    amount = forms.IntegerField(min_value=0)
    payement_due = forms.DateField(label='Date de payement',
                                   widget=forms.DateInput(
                                       attrs={'type': 'date'}))
    status = forms.BooleanField(label='contrat en cours', required=False)


class EventForm(forms.Form):
    support_contact = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='support'), label='support')
    attendees = forms.IntegerField(min_value=0, label='Jauge')
    event_date = forms.DateTimeField(label='Date', widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}))
    note = forms.CharField(max_length=1024, label='Note')


class EventEditForm(forms.Form):
    attendees = forms.IntegerField(min_value=0, label='Jauge')
    event_date = forms.DateTimeField(label='Date', widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}))
    note = forms.CharField(max_length=1024, label='Note')
    event_status = forms.BooleanField(label='status', required=False)
