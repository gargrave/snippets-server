from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Tag, TagSnippetRelation
from .serializers import TagSerializer, TagSnippetRelationWriteSerializer


class TagList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.

    URL looks like:
    api/v1/tags/

    GET request to list a user's Tags
    POST request with Tag data to create a Tag

    Payload for creating a Tag should conform to the following:
    {
        title: [string, max=100]
    }
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagDeleteView(generics.DestroyAPIView):
    """
    Concrete view for deleting an existing Tag, along with all of its
    associated TagSnippetRelations.

    URL looks like:
    api/v1/tags/delete/<pk>
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)


class TagSnippetRelationCreateView(generics.CreateAPIView):
    """
    Concrete view for creating a new TagSnippetRelation (i.e. adding an existing
    Tag to an existing Snippet).

    POST request should look like the following.
    It must contain at least one of the two optional fields:
    {
        _tag: [number] (optional, pk of an existing Tag)
        _snippet: [number] (required, pk of an existing Snippet)
        tag_title: [string, max=100] (optional, to create a new Tag)
    }
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TagSnippetRelationWriteSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override of default create() method to
        provide heavily customized behavior
        """
        # build custom dataset for the serializer based on the type of request
        request_tag_id = request.data.get('_tag')
        request_snippet_id = request.data.get('_snippet')

        ########################################################
        # Look for an existing identical entry before creating
        ########################################################
        try:
            # look for an existing TagSnippetRelation with these values
            existing_entry = TagSnippetRelation.objects.filter(
                owner__pk=self.request.user.pk,
                _tag=request_tag_id,
                _snippet=request_snippet_id
            ).get()
            # if found, get the associate Tag object
            existing_entry_tag = Tag.objects.filter(
                owner__pk=self.request.user.pk,
                pk=request_tag_id).get()
            # manually build a response and simply send back the found data
            return Response({
                'id': existing_entry.pk,
                '_tag': {
                    'id': existing_entry_tag.pk,
                    'title': existing_entry_tag.title
                }
            }, status=status.HTTP_200_OK)
        ########################################################
        # Create a new entry if none was found
        ########################################################
        except TagSnippetRelation.DoesNotExist:
            # if a 'tag_title' was provided in the request, we will use that
            # for the lookup, and create a new Tag if necessary
            if request.data.get('tag_title'):
                tag, created = Tag.objects.get_or_create(
                    owner=request.user,
                    title=request.data.get('tag_title'))
                request_tag_id = tag.pk
            new_entry_data = {
                '_tag': request_tag_id,
                '_snippet': request_snippet_id,
            }
            # now use these settings to create a new TagSnippetRelation
            serializer = self.get_serializer(data=new_entry_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            # manually build a response and simply send back the Tag data
            tag_obj = Tag.objects.get(pk=serializer.data.get('_tag'))
            res_data = {
                'id': serializer.data.get('id'),
                '_tag': {
                    'id': tag_obj.pk,
                    'title': tag_obj.title
                }
            }
            return Response(res_data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)


class TagSnippetRelationDeleteView(generics.GenericAPIView):
    """
    Concrete view for deleting a TagSnippetRelation instance.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return TagSnippetRelation.objects\
            .filter(owner__pk=self.request.user.pk)

    def delete(self, request, *args, **kwargs):
        try:
            # find the Snippet that matches owner/tag/snippet ids
            tag_id = request.data.get('tag_id')
            snippet_id = request.data.get('snippet_id')
            instance = TagSnippetRelation.objects.filter(
                owner__pk=request.user.pk,
                _tag__pk=tag_id,
                _snippet__pk=snippet_id).get()
            instance.delete()
        except TagSnippetRelation.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
