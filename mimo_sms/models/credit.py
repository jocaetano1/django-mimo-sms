from decimal import Decimal

from django.utils.formats import number_format
from django.db import models

from .behaviors import TimeStamp


class Activity(TimeStamp):

    class Types(models.TextChoices):
        ADD = ('1', 'ADD')
        CREDIT = ('2', 'CREDIT')
        DEBIT = ('3', 'DEBIT')
        INVALID = ('4', 'INVALID')

    user = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    voucher = models.CharField(max_length=14)
    credits = models.IntegerField('Credits', default=0)
    type = models.CharField(
        'Type', max_length=1,
        choices=Types.choices, default=Types.ADD)
    price = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'))
    current_credicts = models.IntegerField(default=0)
    status = models.CharField(max_length=1, null=True, blank=True)
    expriration_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'mimo_activitys'
        verbose_name = 'credit'
        verbose_name_plural = 'Credits'

    @property
    def price_format(self):
        return number_format(self.price, 2, force_grouping=True)

    def __str__(self):
        return self.voucher
