from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ImageSerializer
from .models import Image
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions
from oauth2_provider.contrib.rest_framework import TokenHasScope


class ImageListCreate(ListCreateAPIView): # POST/GET methods
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser] # to accept any media types during POST request
    filterset_fields = ['title', 'caption']
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['images']


class ImageRetrieveDestroyDetailView(RetrieveUpdateDestroyAPIView): # GET{id}/DELETE/PUT methods
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['image']
