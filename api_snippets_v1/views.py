from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics, mixins, parsers, permissions, renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer


def index(request):
    return render(request, 'index.html')


class SnippetList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
