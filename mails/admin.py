from django.contrib import admin

from mails.models import (
    Server,
    Mailbox,
    Message,
    PinnedFile,
)


admin.site.register(Server)
admin.site.register(Mailbox)
admin.site.register(Message)
admin.site.register(PinnedFile)
