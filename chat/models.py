from django.db import models
from django.contrib.auth import get_user_model

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = get_user_model()

class MessageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user',
                             related_name='from_user', db_index=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='recipient',
                                  related_name='to_user', db_index=True)
    
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False, 
                                     db_index=True)
    body = models.TextField('body')

    def __str__(self) -> str:
        return str(self.id)
    
    def characters(self):
        """
        Function to return len of body.
        """
        return len(self.body)
    
    def notify_ws_clients(self):
        """
        Inform client there is a new message.
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
        Trims white spaces, saves the message and notifies the recipient via WS if the 
        message is new.
        """
        new = self.id
        self.body = self.body.strip()
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    class Meta:
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
    