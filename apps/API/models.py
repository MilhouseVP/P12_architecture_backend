from django.db import models
from apps.authenticate.models import CustomUser as User


class Customer(models.Model):
    """
    Customer model
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, null=True)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sale_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                                     null=True)
    existing = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.company}, {self.first_name} {self.last_name}'


class Contract(models.Model):
    """
    Contract model
    """
    sale_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                                     null=True)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    amount = models.IntegerField()
    payement_due = models.DateField()
    event_created = models.BooleanField(default=False)

    def __str__(self):
        return f'Contrat {self.id}, {self.customer.company}.'



class Event(models.Model):
    """
    Event model
    """
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                                        null=True)
    event_status = models.BooleanField(default=True)
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE,
                                 null=True)
    attendees = models.IntegerField(default=0)
    event_date = models.DateTimeField(default=date_created)
    note = models.CharField(max_length=1024)

    def __str__(self):
        return f'{self.contract.customer.company}, le {self.event_date}'