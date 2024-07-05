from django.urls import re_path

from mails.consumers import MessageConsumer

websocket_urlpatterns = [
    re_path("ws/messages/", MessageConsumer.as_asgi()),
]
