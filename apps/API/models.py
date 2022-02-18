from django.db import models
from apps.authenticate.models import CustomUser as User




class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sale_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                                     null=True)
    existing = models.BooleanField(default=False)


class Contract(models.Model):
    sale_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                                     null=True)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.IntegerField()
    payement_due = models.DateField()


class Event(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                                        null=True)
    event_status = models.ForeignKey(to=Contract, on_delete=models.CASCADE)
    attendees = models.IntegerField(default=0)
    event_date = models.DateTimeField(default=date_created)
    note = models.CharField(max_length=1024)
