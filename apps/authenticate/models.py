from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom User model extending AbtractUser
    """
    MANAGER = 'manager'
    SALES = 'sales'
    SUPPORT = 'support'

    ROLE_LIST = (
        (MANAGER, 'manager'),
        (SALES, 'sales'),
        (SUPPORT, 'support')
    )

    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, null=True)
    role = models.CharField(max_length=16, choices=ROLE_LIST, default=SUPPORT)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def is_manager(self):
        return self.groups.filter(name='manager').exists()

    def is_sales(self):
        return self.groups.filter(name='sales').exists()

    def is_support(self):
        return self.groups.filter(name='support').exists()