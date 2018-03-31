import logging

from django.contrib.auth.models import User
from django.db import models

LOGGER = logging.getLogger(__name__)

class Employee(models.Model):
    WORKER = 'worker'
    MANAGER = 'manager'
    FINANCE_MANAGER = 'finance_manager'
    EMPLOYEE_TYPE_CHOICES = (
        (WORKER, WORKER),
        (MANAGER, MANAGER),
        (FINANCE_MANAGER, FINANCE_MANAGER),
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='employee', 
                                default=None, db_index=True)
    employee_type = models.CharField(max_length=32, choices=EMPLOYEE_TYPE_CHOICES, default=WORKER,
                              db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u'{0} {1}'.format(self.user.first_name, self.user.last_name)
