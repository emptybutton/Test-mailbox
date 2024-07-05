from django.db import models


class Server(models.Model):
    imap_host = models.CharField(max_length=256)
    imap_port = models.PositiveIntegerField()


class Mailbox(models.Model):
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="mailboxes",
    )
    login = models.CharField(max_length=256)
    password_hash = models.CharField(max_length=1024)


class Message(models.Model):
    subject = models.CharField(max_length=256)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    text = models.CharField(max_length=1024)
    mailbox = models.ForeignKey(
        Mailbox,
        on_delete=models.CASCADE,
        related_name="messages",
    )


class PinnedFile(models.Model):
    file = models.FileField(upload_to="pinned_files/")
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="files",
    )
