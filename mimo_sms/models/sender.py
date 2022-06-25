from django.db import models

from .behaviors import TimeStamp


class Sender(TimeStamp):

    class Status(models.TextChoices):
        ENABLE = ('1', 'ENABLE')
        DISABLED = ('2', 'DISABLED')

    sender = models.CharField(max_length=11, db_index=True)
    reason = models.TextField(max_length=100, default="")
    status = models.CharField(max_length=8, choices=Status.choices)
    default = models.BooleanField('Pattern', default=False)

    class Meta:
        db_table = 'mimo_senders'

    @property
    def is_available(self):
        return self.get_status_display()

    @property
    def name(self):
        return self.sender

    def __str__(self):
        return self.sender
