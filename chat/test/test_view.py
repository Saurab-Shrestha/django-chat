from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from chat.models import MessageModel

User = get_user_model()

class MessageModelViewSetTest(APITestCase):
    
    def setUp(self):
        print("'====================Running setup for Chat view test'====================")
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')
        self.message1 = MessageModel.objects.create(user=self.user1, recipient=self.user2, body="Hello User2")
        self.message2 = MessageModel.objects.create(user=self.user2, recipient=self.user1, body="Hello User1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_messages(self):
        print("'====================Running test_list_messages'====================")
        url = reverse('message-api-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_list_messages_with_target(self):
        print("'====================Running test_list_messages_with_target'====================")
        url = reverse('message-api-list') + '?target=user2@example.com' 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_message(self):
        print("'====================Running test_retrieve_message'====================")
        url = reverse('message-api-detail', kwargs={'pk': self.message1.id})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_message_not_allowed(self):
        print("'====================Running test_retrieve_message_not_allowed'====================")
        # Attempt to retrieve a message not involving user1
        url = reverse('message-api-detail', kwargs={'pk': self.message2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
