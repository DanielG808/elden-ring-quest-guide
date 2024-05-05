from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .serializers import UserSerializer


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Http404:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    return wrapper
        


@api_view(['POST'])
@handle_exceptions
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    user.save()
    token, created = Token.objects.get_or_create(user=user)
    if not created:
        user.auth_token.delete()
        token = Token.objects.create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['POST'])
@handle_exceptions
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        confirm = request.data.get('confirm')

        if password != confirm:
            return Response({'error': 'Passwords do not match.'})
        
        serializer.save()
        user = CustomUser.objects.get(username=request.data['username'])
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@handle_exceptions
def logout(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token_parts = auth_header.split()
        if len(token_parts) == 2:
            token = token_parts[1]
            try:
                auth_token = Token.objects.get(key=token)
                user = auth_token.user
                user.save()
                auth_token.delete()
                return Response({'detail': 'Logged out successfully.'})
            except Token.DoesNotExist:
                return Response({'detail': 'Token does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'detail': 'Token not provided in request headers.'}, status=status.HTTP_400_BAD_REQUEST)



