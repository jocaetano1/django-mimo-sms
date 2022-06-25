import requests

from mimo_sms.models.credit import Activity
from mimo_sms.api import Mimo, MimoMessage
from mimo_sms.models.message import Message, Recipient

mimo_obj = Mimo()
mimo_sms_obj = MimoMessage()


def charge_credits(voucher: str):
    """Charge accounts of user using voucher code."""
    url = mimo_obj._make_url('credit/recharge')
    res = requests.get(url, params={'voucher': voucher})
    if res.status_code == 201:
        data = res.json()
        credit_obj = Activity.objects.create(
            user=data.get('user'),
            serial_number=data.get('serialNumber'),
            voucher=data.get('voucher'),
            credits_=data.get('credits_'),
            price=data.get('price'),
            status=data.get('status'),
            current_credits=data.get('currentCredits'),
            expiration_time=data.get('expirationTime')
        )
        return credit_obj

    credit_obj = Activity.objects.create(
        voucher=voucher,
        type=Activity.Types.INVALID
    )
    return credit_obj


def view_credits():
    """View the credit of user."""
    url = mimo_obj._make_url('credit/')
    res = requests.get(url)
    return res.json()


def transfer_credits(username: str, balance: int):
    """View the credit of user."""
    url = mimo_obj._make_url('credit/transfer')
    res = requests.get(url, params={'username': username, 'balance': balance})
    return res.json()


def send_sms(**payload):
    """Send text messages via MIMO.

    :param sender: An sender by MIMO or None
    :param text: Text as a body of message
    :param recipients: list of phone's numbers
    """
    res = mimo_sms_obj.send(**payload)
    if 'sender' in res.keys():
        message_obj = Message.objects.create(
            sender=res.get('sender'),
            text=res.get('text'),
            size=res.get('size'),
            unicode=res.get('unicode')
        )
        list_items = []
        items = res.get('recipients')
        for item in items:
            recipient_obj = Recipient()
            recipient_obj.message_id = message_obj.id
            recipient_obj.message_id = item.get('messageId')
            recipient_obj.phone = item.get('phone')
            recipient_obj.status = item.get('status')
            list_items.append(recipient_obj)
        Recipient.objects.bulk_create(list_items)
        return message_obj
