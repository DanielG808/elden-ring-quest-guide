from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import User
from .serializers import UserSerializer


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Http404:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper


@api_view(['POST'])
@handle_exceptions
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
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
        password = request.data['password']
        confirm = request.data['confirm']
        if password != confirm:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.create(serializer.validated_data)
        user.set_password(request.data['password'])
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
                auth_token.delete()
                return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'error': 'Token does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        else: return Response({'error': 'Invalid Authorization header format.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Authorization header not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    

class UserView(APIView):
    @handle_exceptions
    def get(self, request, token=None):
        if token:
            try:
                auth_token = Token.objects.get(key=token)
                user = auth_token.user
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'error': 'Token does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    @handle_exceptions
    def put(self, request, token):
        try:
            auth_token = Token.objects.get(key=token)
            user = auth_token.user
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exist.'}, status=status.HTTP_401_UNAUTHORIZED)