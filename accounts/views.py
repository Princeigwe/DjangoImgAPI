from django.shortcuts import render
from .serializers import UserSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions, generics
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class UserListAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = [''] # scope the token must have to make a GET and POST request on users
    queryset = User.objects.all()
    serializer_class = UserSerializer
