from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            is_active=True
        )
        self.client = APIClient()
        self.token = RefreshToken.for_user(self.user).access_token

    def test_register(self):
        print("================Running test_register================")
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login(self):
        print("================Running test_login================")
        url = reverse('token_obtain_pair')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_user_details(self):
        print("================Running test_get_user_details================")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('user_details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_logout(self):
        print("================Running test_logout...================")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('logout')
        refresh_token = str(RefreshToken.for_user(self.user))
        data = {'refresh_token': refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_list(self):
        print("================Running test_user_list================")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)