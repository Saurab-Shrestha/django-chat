from django.db import IntegrityError
from django.test import TestCase
from chat.models import MessageModel
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageTestCase(TestCase):
    """
    Test cases for MessageModel
    """
    def setup(self):
        self.test_user1 = User.objects.create(email='ram@email.com')
        self.test_user2 = User.objects.create(email='shyam@email.com')

    def test_message_user(self):
        message = MessageModel.objects.create(
                    user=self.test_user1,
                    recipient=self.test_user2,
                    body='test message'
                )
        self.assertEqual(message.user.email, 'shyam@email.com')
        self.assertEqual(message.body, 'test')
        self.assertEqual(message.characters(), '12')
        
    def test_message_no_user(self):
        with self.assertRaises(IntegrityError):
            MessageModel.objects.create(user=None, body='test')

    def test_message_create_retrieve(self):
        mid = MessageModel.objects.create(user=self.test_user1,
                                          recipient=self.test_user2,
                                          body='tbody').id
        msg = MessageModel.objects.get(id=mid)
        # Asserts
        self.assertEqual(msg.characters(), 5)
        self.assertEqual(msg.body, 'tbody')
        self.assertEqual(msg.user, self.test_user1)
        self.assertEqual(msg.recipient, self.test_user2)

