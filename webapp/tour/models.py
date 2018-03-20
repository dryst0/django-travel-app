import logging

from django.db import models

from employee.models import Employee

LOGGER = logging.getLogger(__name__)

class Transport(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            help_text=u'Type of Transport')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Tour(models.Model):
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    REQUEST_FOR_INFORMATION = 'request_for_information'
    SUBMITTED_TO_FINANCE = 'submitted_to_finance'
    APPROVAL_STATUS_CHOICES = (
        (DRAFT, DRAFT),
        (SUBMITTED, SUBMITTED),
        (APPROVED, APPROVED),
        (REJECTED, REJECTED),
        (REQUEST_FOR_INFORMATION, REQUEST_FOR_INFORMATION),
        (SUBMITTED_TO_FINANCE, SUBMITTED_TO_FINANCE),
    )

    description = models.TextField(null=True, blank=True, default='')
    start_date = models.DateField(
        db_index=True, null=False, blank=False,
        help_text=u'Date when employees will start their tour')
    end_date = models.DateField(
        db_index=True, null=False, blank=False,
        help_text=u'Date when employees will end their tour')
    transport = models.ForeignKey(Transport, on_delete=models.PROTECT, related_name='tour',
                                  db_index=True)
    ticket_cost = models.PositiveIntegerField(default=0)
    home_cab_cost = models.PositiveIntegerField(default=0)
    dest_cab_cost = models.PositiveIntegerField(default=0)
    hotel_cost = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=32, choices=APPROVAL_STATUS_CHOICES, default=DRAFT,
                              db_index=True)
    created_by_user = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                        related_name='created_by_tour', db_index=True)
    approved_by_user = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                         related_name='approved_by_tour', null=True, blank=True,
                                         default=None, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
