from dataclasses import dataclass
import email
import imaplib
from typing import Iterable, Optional

from django.contrib.auth.hashers import check_password

from mails.models import Message, Mailbox, PinnedFile


class MailboxGateway:
    @classmethod
    def get_by(cls, login: str) -> Optional[Mailbox]:
        return Mailbox.objects.filter(login=login).first()


class LoginError(Exception): ...


class IMAPServerGateway:
    @classmethod
    def read_unread_messages_form(cls, mailbox: Mailbox) -> Iterable[Message]:
        server = mailbox.server
        imap = imaplib.IMAP4_SSL(server.imap_host, server.imap_port)

        try:
            imap.login(mailbox.login, password)
        except Exception as error:
            raise LoginError from error

        _, result = imap.search(None, 'X-GM-RAW "search SEEN UNSEEN"')
        message_ids = result[0].split()

        for message_id in message_ids:
            _, message_data = imap.fetch(message_id, '(RFC822)')
            raw_message = email.message_from_bytes(message_data[0][1])

            subject = raw_message['Subject']
            sent_date = raw_message['Date']
            received_date = raw_message['Received'].splitlines()[-1]
            text = IMAPServerGateway._body_of(raw_message)

            message = Message(
                subject=subject,
                sent_date=sent_date,
                received_date=received_date,
                text=text,
                mailbox=mailbox,
            )

            files = _files_of(raw_message, message)
            message.files = files

            yield message

        imap.close()
        imap.logout()

    @classmethod
    def _body_of(raw_message) -> str:
        if not raw_message.is_multipart():
            return raw_message.get_payload(decode=True).decode('utf-8')

        for part in raw_message.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode('utf-8')

    @classmethod
    def _files_of(cls, raw_message, message: Message) -> tuple[PinnedFile, ...]:
        return tuple(
            PinnedFile(
                file=part.get_payload(decode=True),
                message=message,
            )
            for part in msg.walk()
            if part.get_content_type().startswith('application/')
        )
