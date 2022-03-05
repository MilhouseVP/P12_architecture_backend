from django import forms


class EventForm(forms.Form):
    customer = forms.IntegerField()
    support_contact = forms.IntegerField()

