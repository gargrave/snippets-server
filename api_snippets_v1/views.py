from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import generics, mixins, parsers, permissions, renderers
from rest_framework.response import Response

from .models import Snippet
from .serializers import SnippetSerializer


def index(request):
    return render(request, 'index.html')


class SnippetList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
