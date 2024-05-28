from django.db import IntegrityError
from django.test import TestCase
from chat.models import MessageModel
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageTestCase(TestCase):
    """
    Test cases for MessageModel
    """
    print('================Setting up Test for MessageModel====================')
    def setUp(self):
        self.test_user1 = User.objects.create(email='ram@email.com', password='password123')
        self.test_user2 = User.objects.create(email='shyam@email.com', password='password123')

    def test_message_user(self):
        print("================Running test_message_user================")
        message = MessageModel.objects.create(
                    user=self.test_user1,
                    recipient=self.test_user2,
                    body='test message'
                )
        self.assertEqual(message.user.email, 'ram@email.com')
        self.assertEqual(message.body, 'test message')
        self.assertEqual(message.characters(), 12)
        
    def test_message_no_user(self):
        print("================Running test_message_no_user================")
        with self.assertRaises(IntegrityError):
            MessageModel.objects.create(user=None, recipient=self.test_user2, body='test message')

    def test_message_create_retrieve(self):
        print("================Running test_message_create_retrieve================")
        mid = MessageModel.objects.create(user=self.test_user1,
                                          recipient=self.test_user2,
                                          body='tbody').id
        msg = MessageModel.objects.get(id=mid)
        self.assertEqual(msg.characters(), 5)
        self.assertEqual(msg.body, 'tbody')
        self.assertEqual(msg.user, self.test_user1)
        self.assertEqual(msg.recipient, self.test_user2)