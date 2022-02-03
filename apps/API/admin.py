from django.contrib import admin
from apps.API.models import Customer, Contract, Event


admin.site.register(Contract)
admin.site.register(Customer)
admin.site.register(Event)