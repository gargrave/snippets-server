from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

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
                .filter(owner=self.request.user) \
                .exclude(archived=True)
        else:
            self.queryset = Snippet.objects \
                .filter(owner=self.request.user) \
                .filter(title__icontains=search_query)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetAdvancedSearch(mixins.ListModelMixin,
                            generics.GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SnippetSerializer

    def post(self, request, *args, **kwargs):
        # if a 'search' query param is provided, filter by that value
        search_by_title = request.data.get('title', '')
        search_by_tags = request.data.get('tags', '')

        # TODO clean this up
        if search_by_title != '' and search_by_tags == '':
            self.queryset = Snippet.objects \
                .filter(owner=self.request.user,
                        title__icontains=search_by_title)
        elif search_by_title == '' and search_by_tags != '':
            self.queryset = Snippet.objects \
                .filter(owner=self.request.user,
                        tags___tag__title__iexact=search_by_tags)
        elif search_by_title != '' and search_by_tags != '':
            self.queryset = Snippet.objects \
                .filter(owner=self.request.user,
                        title__icontains=search_by_title,
                        tags___tag__title__iexact=search_by_tags)
        else:
            self.queryset = Snippet.objects \
                .filter(owner=self.request.user)
        return self.list(request, *args, **kwargs)


class ArchivedSnippetList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Snippet.objects \
            .filter(owner=self.request.user) \
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
        self.queryset = Snippet.objects \
            .filter(owner=self.request.user) \
            .exclude(starred=False)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
