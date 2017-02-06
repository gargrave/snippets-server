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
    Concrete view for listing Snippets based on multiple search criteria.

    POST request should take the following form (all fields are optional,
        and if no fields are provided, the list will simply be all Snippets).
    {
        title: [string]
        tags: [string] (comma-separated list of strings to search by; any empty
            or whitespace string are ignored)
    }
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SnippetSerializer

    def post(self, request, *args, **kwargs):
        # if a 'search' query param is provided, filter by that value
        search_by_title = request.data.get('title', '')
        search_by_tags = request.data.get('tags', '')

        # basic query: initially list all of this User's Snippets
        self.queryset = Snippet.objects.filter(owner=self.request.user)

        # if title search is provided, add to query
        if search_by_title != '':
            self.queryset = self.queryset \
                .filter(title__icontains=search_by_title)

        # if tags are provided, split/clean them, and add to query
        if search_by_tags != '':
            tags_list = search_by_tags.split(',')
            for tag in [t for t in tags_list if not t.isspace()]:
                self.queryset = self.queryset \
                    .filter(tags___tag__title__iexact=tag.strip())

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
