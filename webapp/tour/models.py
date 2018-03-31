import logging

from django.db import models

from employee.models import Employee

LOGGER = logging.getLogger(__name__)

class Currency(models.Model):
    USD = 'usd'
    SGD = 'sgd'
    PHP = 'php'
    CURRENCY_TYPE_CHOICES = (
        (USD, USD),
        (SGD, SGD),
        (PHP, PHP)
    )
    currency = models.CharField(max_length=32, choices=CURRENCY_TYPE_CHOICES, default=PHP,
                                db_index=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Currency: id={0}, currency={1}".format(self.pk, self.currency)

class Transport(models.Model):
    PLANE = 'plane'
    SHIP = 'ship'
    BUS = 'bus'
    TRANSPORT_TYPE_CHOICES = (
        (PLANE, PLANE),
        (SHIP, SHIP),
        (BUS, BUS),
    )
    name = models.CharField(max_length=64, unique=True, db_index=True,
                            help_text=u'Type of Transport')
    transport_type = models.CharField(max_length=32, choices=TRANSPORT_TYPE_CHOICES, default=PLANE,
                                      db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Transport: id={0}, name={1}, type={2}".format(self.pk, self.name,
                                                              self.transport_type)

class Ticket(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='ticket',
                                  db_index=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='ticket',
                                 db_index=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Ticket: id={0}, type={1}, cost={2}".format(self.pk, self.transport.name, self.cost)

class Hotel(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True,
                            help_text=u'Name of Hotel')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Hotel: id={0}, name={1}".format(self.pk, self.name)

class HotelCost(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_cost',
                                 db_index=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='hotel_cost',
                                 db_index=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Hotel: id={0}, name={1}, currency={2}, cost={3}".format(self.pk, self.hotel.name, self.currency, self.cost)

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

    description = models.TextField(default='')
    start_date = models.DateField(
        db_index=True, null=False, blank=False,
        help_text=u'Date when employees will start their tour')
    end_date = models.DateField(
        db_index=True, null=False, blank=False,
        help_text=u'Date when employees will end their tour')
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='tour',
                                  null=True)
    home_cab = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    dest_cab = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    hotel_cost = models.ForeignKey(HotelCost, on_delete=models.CASCADE, related_name='tour',
                              null=True)
    status = models.CharField(max_length=32, choices=APPROVAL_STATUS_CHOICES, default=DRAFT,
                              db_index=True)
    worker = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='tour_worker',
                               null=True, db_index=True)
    manager = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='tour_manager',
                                db_index=True)
    finance_manager = models.ForeignKey(Employee, on_delete=models.PROTECT,
                                        related_name='tour_finance_manager', null=True, blank=True,
                                        db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u'Tour {0}: (Start Date: {1}, End Date: {2}, Status: {3})'.format(self.pk,
                                                                                 self.start_date,
                                                                                 self.end_date,
                                                                                 self.status)
