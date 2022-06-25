import os
import requests

from django.conf import settings


class Mimo:
    """
    Basic communication with the MIMO service.
    """

    def __init__(self) -> None:
        if 'MIMO_API_TOKEN' and 'MIMO_API_HOST' in os.environ.keys():
            self.__TOKEN = os.environ['MIMO_API_TOKEN']
            self.__HOST = os.environ['MIMO_API_HOST']
        else:
            try:
                self.__TOKEN = settings.MIMO_API_TOKEN
                self.__HOST = settings.MIMO_API_HOST
            except AttributeError as e:
                raise e

    def logout(self):
        url = self._make_url('user/logout')
        res = requests.get(url)
        return res.json()

    def _get_hostname(self):
        return self.__HOST

    def _get_token(self):
        return self.__TOKEN

    def _make_url(self, endpoint: str):
        host = self._get_hostname()
        if host.endswith("/"):
            host.removesuffix("/")
        return f"{host}{endpoint}?token={self._get_token()}"

    def _join(self, *elements):
        return ','.join(*elements)


class MimoSender(Mimo):
    """Communication with sender resource."""

    def __init__(self):
        super().__init__()

    def list(self, requested: bool = False, /):
        """List all senders registred in MIMO."""
        if requested is False:
            url = self._make_url('sender-id/list-all')
        else:
            url = self._make_url('sender-id/list-all/requested')
        res = requests.get(url)
        return res.json()

    def create(self, **payload):
        """Create a new sender."""
        url = self._make_url('sender-id/request')
        res = requests.post(url, json=payload)
        return res.json()

    def view(self, sender_name: str, make_default: bool = False, /):
        """Retrive all information about sender."""
        if make_default is True:
            url = self._make_url('sender-id/default')
            res = requests.get(url, params={'sender': sender_name})
        else:
            url = self._make_url('sender-id/list-one')
            res = requests.get(url, params={'sender': sender_name})
        return res.json()

    def delete(self, senders_ids: list = None):
        """Delete an sender."""
        url = self._make_url('sender-id/delete')
        senders = self._join(senders_ids)
        res = requests.get(url, params={'senders': senders})
        return res.json()


class MimoMessage(Mimo):
    """Communication with SMS resource."""

    def __init__(self):
        super().__init__()

    def send(self, sender: str, recipients: list, text) -> int:
        """Send messages for an list of recipients."""
        url = self._make_url('message/send')
        receivers = self._join(recipients)
        payload = {
            'sender': sender,
            'recipients': receivers,
            'text': text
        }
        res = requests.post(url, json=payload)
        return res.json()

    def all(self):
        """Retrive all messages in MIMO SMS."""
        url = self._make_url('message/list-all')
        res = requests.get(url)
        return res.json()

    def list_by_phone(self, phone, /):
        """List messages by phone number."""
        url = self._make_url('message/list-all/by-recipient')
        res = requests.get(url, params={'phone': phone})
        return res.json()

    def list_by_date(self, start_date, end_date, /):
        """List messages by date."""
        url = self._make_url('message/list-all/by-date')
        params = {'start-date': start_date, 'end-date': end_date}
        res = self.get(url, params=params)
        return res.json()

    def list_recipients(self):
        """List all recipients of all messages send by one user."""
        url = self._make_url('message/list-all/recipients')
        res = requests.get(url)
        return res.json()

    def check_status(self, id: int = None, /):
        """Check the status of message."""
        url = self._make_url('message/list-one')
        res = requests.get(url, params={'id': id})
        return res.json()

    def delete(self, messages_ids: list = None):
        """Delete all messages or basead in IDs."""
        if messages_ids is None:
            url = self._make_url('message/delete/all')
            res = requests.get(url)
        else:
            url = self._make_url('message/delete')
            ids = self._join(messages_ids)
            res = requests.get(url, params={'ids': ids})
        return res.json()


class MimoContact(Mimo):
    """Communication with contacts resource."""

    def __init__(self):
        super().__init__()

    def list(self):
        """List all contacts registered in MIMO."""
        url = self._make_url('contact/list-all')
        res = requests.get(url)
        return res.json()

    def create(self, **payload):
        """Create one contact in MIMO."""
        url = self._make_url('contact/add')
        res = requests.post(url, json=payload)
        return res.json()

    def update(self, **payload):
        """Update one contact in MIMO."""
        url = self._make_url('contact/edit')
        res = requests.post(url, json=payload)
        return res.json()

    def view(self, phone_number: str):
        """Retrive one contact basead in phone number."""
        url = self._make_url('contact/list-one')
        res = requests.get(url, params={'phone': phone_number})
        return res.json()

    def delete(self, phones_numbers: list = None):
        """
        Delete all contacts or once list 
        of contacts basead in phones numbers.
        """
        if phones_numbers is None:
            url = self._make_url('contact/delete/all')
            res = requests.get(url)
            return res.json()
        else:
            url = self._make_url('contact/delete')
            phones = self._join(phones_numbers)
            res = requests.get(url, params={'phones': phones})
            return res.json()


class MimoGroup(Mimo):
    """Communication with groups resource."""

    def __init__(self):
        super().__init__()

    def list(self):
        """List all groups in MIMO Service."""
        url = self._make_url('group/list-all')
        res = requests.get(url)
        return res.json()

    def create(self, name: str, contacts: list = None):
        """Create an group in MIMO."""
        url = self._make_url('group/add')
        payload = {'name': name}
        if contacts is not None:
            payload.update(contacts=contacts)
        res = requests.post(url, json=payload)
        return res.json()

    def add(self, groups_names: list, phones_numbers: list):
        """Add contacts in groups."""
        url = self._make_url('group/add/contacts')
        groups = self._join(groups_names)
        contacts = self._join(phones_numbers)
        res = requests.get(url, params={'groups': groups, 'phones': contacts})
        return res.json()

    def add_from_excel(self, file_name):
        """Add contacts from excel file."""
        url = self._make_url('group/add/contacts')
        files = {'file': (file_name, open(file_name, 'rb'))}
        res = requests.post(url, files=files)
        return res.json()

    def update(self, **payload):
        """Update information of group."""
        if 'name' and 'new_name' in payload.keys():
            url = self._make_url('group/edit/name')
            params = {
                'name': payload.get('name'),
                'new-name': payload.get('new_name')
            }
            res = requests.get(url, params=params)
        else:
            url = self._make_url('group/edit')
            res = requests.post(url, json=payload)
        return res.json()

    def view(self, name: str):
        """View an expecific group."""
        url = self._make_url('group/list-one')
        res = requests.get(url, params={'name': name})
        return res.json()

    def delete(self, groups_names: list = None):
        """Delete all information about an group."""
        if groups_names is None:
            url = self._make_url('group/delete/all')
            res = requests.get(url)
            return res.json()
        else:
            url = self._make_url('group/delete')
            groups = self._join(groups_names)
            res = requests.get(url, params={'names': groups})
            return res.json()


class MimoCampain(Mimo):
    """Communication with campaigns resource."""

    def __init__(self):
        super().__init__()

    def list(self):
        """List all campains in MIMO."""
        url = self._make_url('note/list-all')
        res = requests.get(url)
        return res.json()

    def create(self, **payload):
        """Create an new campain in MIMO."""
        url = self._make_url('note/add')
        res = requests.post(url, json=payload)
        return res.json()

    def update(self, **payload):
        """Update attrs of an campain in MIMO."""
        url = self._make_url('note/edit')
        res = requests.post(url, json=payload)
        return res.json()

    def view(self, title: str):
        """Retrive an specific campain in MIMO."""
        url = self._make_url('note/')
        res = requests.get(url, params={'title': title})
        return res.json()

    def delete(self, titles_names: list):
        """Delete all campain or Specific campain by titles."""
        if titles_names is None:
            url = self._make_url('note/delete/all')
            res = requests.get(url)
            return res.json()
        else:
            url = self._make_url('note/delete')
            titles = self._join(titles_names)
            res = requests.get(url, params={'titles': titles})
            return res.json()
