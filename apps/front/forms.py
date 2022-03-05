from django import forms
from apps.API.models import Customer, Contract
from apps.authenticate.models import CustomUser


class EventForm(forms.Form):
    # customer = forms.ModelChoiceField(queryset=Customer.objects.all(),
    #                                   label='client')
    support_contact = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='support'), label='support')
    # contract = forms.ModelChoiceField(queryset=Contract.objects.all(),
    #                                   label='Contrat')
    attendees = forms.IntegerField(min_value=0, label='Jauge')
    event_date = forms.DateTimeField(label='Date')
    note = forms.CharField(max_length=1024, label='Note')
