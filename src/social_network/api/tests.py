from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social_user.models import User

class UserTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_user_success(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'NewPassword123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])

    def test_register_user_invalid_data(self):
        data = {
            'email': '',
            'password': 'short',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Successfully logged in')

    def test_user_login_invalid_credentials(self):
        data = {
            'email': 'notvalid@email.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')
