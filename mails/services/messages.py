from typing import Iterable

from django.contrib.auth.hashers import check_password

from mails.models import Message
from mails.data_access.gateways import MailboxGateway, IMAPServerGateway, LoginError


class NoAccessToMailboxError(Exception): ...

class NoAccessToServerError(Exception): ...


def load_new_messages(login: str, password: str) -> Iterable[Message]:
    mailbox = MailboxGateway.get_by(login)

    if mailbox is None or not check_password(mailbox.password, password):
        raise NoAccessToMailboxError

    messages = IMAPServerGateway.read_unread_messages_form(mailbox)

    try:
        for message in messages:
            message.save()
            yield message
    except LoginError as error:
        raise NoAccessToServerError from error
