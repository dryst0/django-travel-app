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
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='employee',
                             null=True, blank=True, default=None, db_index=True)
    employee_type = models.CharField(max_length=32, choices=EMPLOYEE_TYPE_CHOICES, default=WORKER,
                              db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
