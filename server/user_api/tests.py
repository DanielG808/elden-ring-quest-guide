from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from .models import User


        
class TestRegAuthView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.user_data = {'username': 'test-user-1', 'password': 'test-password-1'}
        self.user = User.objects.create_user(username='test-user-1', password='test-password-1')
        self.token = Token.objects.create(user=self.user)


    def test_registration_view(self):
        # Test registratrion missing username
        invalid_data = {'username': '', 'password': 'test-password-1', 'confirm': 'test-password-1'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Test registratrion missing password
        invalid_data = {'username': 'test-user-2', 'password': '', 'confirm': 'test-password-1'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test registratrion password mismatch
        invalid_data = {'username': 'test-user-2', 'password': 'test-password-1', 'confirm': 'wrong-password'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Passwords do not match.')
        
        # Test registration success
        data = {'username': 'test-user-2', 'password': 'TestPassword85!', 'confirm': 'TestPassword85!'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

        
    def test_logout_view(self):
        # Test logout missing auth
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Authorization header not provided.')

        # Test logout invalid auth format
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Authorization')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid Authorization header format.')

        # Test logout invalid token
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Authorization FAKE_TOKEN')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Token does not exist.')

        # Test logout success
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Authorization {self.token}')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Logged out successfully.')


    def test_login_view(self):
        # Test login invalid username
        url = reverse('login')
        invalid_data = {'username': 'newuser', 'password': 'wrongpassword'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test login invalid password
        url = reverse('login')
        invalid_data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Not found.')

        # Test login success
        url = reverse('login')
        data = self.user_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(len(response.data['token']), len(self.token.key))