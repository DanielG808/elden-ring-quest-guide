from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import CustomUser


@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, id=request.data['id'])
    if not user.check_password(request.data['password']):
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    user.save()
    token, created = Token.objects.get_or_create(user=user)
    if not created:
        user.auth_token.delete()
        token = Token.objects.create(user=user)
    return Response({'token': token.key})
