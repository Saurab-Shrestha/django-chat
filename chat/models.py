from django.db import models
from django.contrib.auth import get_user_model

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = get_user_model()

class MessageModel(models.Model):
    """
    Model representing a chat message.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='user',
        related_name='from_user', 
        db_index=True
    )
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='recipient',
        related_name='to_user', 
        db_index=True
    )
    
    timestamp = models.DateTimeField(
        'timestamp', 
        auto_now_add=True, 
        editable=False, 
        db_index=True
    )
    body = models.TextField('body')

    def __str__(self) -> str:
        return str(self.id)
    
    def characters(self):
        """
        Returns the number of characters in the message body.
        """
        return len(self.body)
    
    def notify_ws_clients(self):
        """
        Notifies WebSocket clients about the new message.
        """
        notification = {
            'type': 'receive_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print(f"User.id = {self.user.id}")
        print(f"Recipient.id = {self.recipient.id}")

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to trim whitespace and notify WebSocket clients about new messages.
        """
        is_new = self.id
        self.body = self.body.strip()
        super(MessageModel, self).save(*args, **kwargs)
        if is_new is None:
            self.notify_ws_clients()

    class Meta:
        """
        Meta class for the Message model.
        """
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
    