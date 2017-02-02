from rest_framework import generics, permissions

from .models import Snippet
from .serializers import SnippetSerializer


class SnippetList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        # if a 'search' query param is provided, filter by that value
        search_query = request.GET.get('search', '')

        if search_query == '':
            self.queryset = Snippet.objects\
                .filter(owner__pk=self.request.user.pk)\
                .exclude(archived=True)
        else:
            self.queryset = Snippet.objects \
                .filter(owner__pk=self.request.user.pk) \
                .filter(title__icontains=search_query)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ArchivedSnippetList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Snippet.objects\
            .filter(owner__pk=self.request.user.pk)\
            .exclude(archived=False)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StarredSnippetList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Snippet.objects\
            .filter(owner__pk=self.request.user.pk)\
            .exclude(starred=False)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
