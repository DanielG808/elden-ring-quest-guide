from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from unittest.mock import patch

from .models import CustomUser
from .serializers import UserSerializer


