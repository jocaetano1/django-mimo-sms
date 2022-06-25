from django.test import TestCase

from mimo_sms.models import (
    Recipient,
    Activity,
    Message,
    Sender
)
from mimo_sms.utils import (
    charge_credits,
    view_credits,
    send_sms
)


class MessageTestCase(TestCase):

    def setUp(self) -> None:
        sender_obj = Sender.objects.create(
            sender='LIVING',
            reason='Test sender reason')
        self.sender = sender_obj

    def test_create_message(self):
        message_obj = Message.objects.create(
            sender=self.sender,
            text="My test message",
        )
        self.message = message_obj
        self.assertEqual(message_obj.id, 1)
        self.assertEqual(message_obj.size, 0)
        self.assertIs(message_obj.unicode, False)

    def test_create_recipients(self):
        message_obj = Message.objects.create(
            sender=self.sender,
            text="My test message",
        )
        recipients = []
        for _ in range(10):
            recipient = Recipient()
            recipient.message = message_obj
            recipient.phone = f"93384389{_}"
            recipient.messageId = "ABA-109-1901"
            recipient.status = "Sending..."
            recipients.append(recipient)
        result = Recipient.objects.bulk_create(recipients)
        self.assertEqual(type(result), list)
        self.assertEqual(Recipient.objects.count(), 10)

    def test_send_message_with_no_credit(self):
        text = "Testing something... @josan"
        recipients = ["930499550"]
        result = send_sms(
            sender=self.sender.name,
            text=text,
            recipients=recipients)
        self.assertEqual(result, None)


class ActivityTestCase(TestCase):

    def test_charge_credits(self):
        res = charge_credits("91919191019191")
        self.assertEqual(res.id, 1)
        self.assertEqual(res.type, Activity.Types.INVALID)

    def test_view_credits_balance(self):
        res = view_credits()
        self.assertDictEqual(res, {'balance': '0'})
