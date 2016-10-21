from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import generics, mixins, parsers, permissions, renderers
from rest_framework.response import Response

from .models import Snippet
from .serializers import SnippetSerializer


def index(request):
    return render(request, 'index.html')


class SnippetList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Snippet.objects.filter(owner__pk=self.request.user.pk)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
