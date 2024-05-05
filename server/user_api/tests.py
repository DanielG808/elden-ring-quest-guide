from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from .models import User


        
class TestRegistrationView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_registration_view(self):
        # Test registratrion missing username
        invalid_data = {'username': '', 'password': 'testpassword', 'confirm': 'testpassword'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Test registratrion missing password
        invalid_data = {'username': 'testuser', 'password': '', 'confirm': 'testpassword'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test registratrion password mismatch
        invalid_data = {'username': 'testuser', 'password': 'testpassword', 'confirm': 'wrongpassword'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Passwords do not match.')

    def test_registration_password_mismatch(self):
        invalid_data = {'username': 'testuser', 'password': 'testpassword', 'confirm': 'wrongpassword'}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Passwords do not match.')

    # Test registration success
        data = {'username': 'testuser', 'password': 'TestPassword85!', 'confirm': 'TestPassword85!'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)


class TestAuthenticationViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'password': 'testpassword'}
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    # LOGIN TESTS

    def test_login_view_invalid_username(self):
        url = reverse('login')
        invalid_data = {'username': 'newuser', 'password': 'wrongpassword'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_login_view_invalid_password(self):
        url = reverse('login')
        invalid_data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Not found.' )


    def test_login_view_sucess(self):
        url = reverse('login')
        data = self.user_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(len(response.data['token']), len(self.token.key))

    # LOGOUT TESTS
        
    def test_logout_view_missing_auth(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Authorization header not provided.')


    def test_logout_view_invalid_auth_format(self):
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Authorization')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid Authorization header format.')


    def test_logout_view_invalid_token(self):
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Authorization FAKE_TOKEN')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Token does not exist.')


    def test_logout_view_success(self):
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Authorization {self.token}')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Logged out successfully.')