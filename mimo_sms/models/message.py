from django.db import models

from .behaviors import TimeStamp


class Message(TimeStamp):
    sender = models.ForeignKey(
        'mimo_sms.Sender', on_delete=models.SET_NULL,
        related_name='messages', null=True, blank=True)
    message_id = models.IntegerField(
        'ID', null=True, blank=True)
    text = models.TextField()
    unicode = models.BooleanField(default=False)
    size = models.IntegerField(default=0)

    class Meta:
        db_table = 'mimo_message'

    @property
    def mimo_message_id(self):
        """ID of MIMO SMS Service."""
        return self.message_id

    def __str__(self):
        return self.text


class Recipient(TimeStamp):

    class Status(models.TextChoices):
        SENT = ('S', 'SENT')
        PENDING = ('P', 'PENDING')
        DELIVERED = ('D', 'DELIVERED')

    message = models.ForeignKey(
        'Message', on_delete=models.CASCADE, related_name='recipients')
    phone = models.CharField(max_length=9, db_index=True)
    messageId = models.CharField('Message ID', max_length=25)
    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.PENDING)

    class Meta:
        db_table = 'mimo_recipients'

    def __str__(self):
        return self.phone
