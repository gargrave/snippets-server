from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Tag
from .serializers import TagSerializer


class TagList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Tag.objects \
            .filter(owner__pk=self.request.user.pk)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
