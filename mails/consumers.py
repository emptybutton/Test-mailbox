import json

from channels.generic.websocket import WebsocketConsumer

from mails.services.messages import (
    load_new_messages, NoAccessToMailboxError
)
from mails.model import Message


class MessageConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text: str) -> None:
        data = json.loads(text)

        try:
            login = str(data.get("login"))
            password = str(data.get("password"))
        except Exception:
            self._panic("InvalidRequestError")
            return

        messages = load_new_messages(login, password)

        try:
            received_messages = list()

            for message in messages:
                received_messages.append(message)
                view = self._counter_delta_view_of(message)
                self.send(text_data=json.dumps(view))

            for message in received_messages:
                view = self._message_view_of(message)
                self.send(text_data=json.dumps(view))

        except NoAccessToMailboxError:
            self._panic("NoAccessError")
            return

        self.close()

    def _panic(self, type_: str) -> None:
        self.send(text_data=json.dumps(self._panic_view_with(type_)))
        self.close()

    def _panic_view_with(self, type_: str) -> dict:
        return {"errorType": type_}

    def _message_view_of(self, message: Message) -> dict:
        return {
            'message': {
                'subject': message.subject,
                'sentDate': message.sent_date.timestamp(),
                'receivedDate': message.received_date.timestamp(),
                'text': _cut(message.text, limit=64),
            }
        }

    def _counter_delta_view_of(self, message: Message) -> dict:
        return {'counterDelta': 1}


def _cut(text: str, *, limit: int) -> str:
    if len(text) <= limit:
        return text

    cut_text = text[:limit]
    return f"{cut_text}..."
