from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Snippet, Tag, TagSnippetRelation, UserProfile

# Get the UserModel
UserModel = get_user_model()


class TagRelatedField(serializers.RelatedField):
    """
    Custom RelatedField serializer for Tags. Simply returns the title of the Tag.
    """
    def to_representation(self, value):
        return value.title


class TagSnippetRelationSerializer(serializers.ModelSerializer):
    """
    Custom serializer for TagSnippetRelation. Note that this also uses
    the custom TagRelatedField to build a front-end friendly version of
    the necessary data.
    """
    _tag = TagRelatedField(read_only=True)

    class Meta:
        model = TagSnippetRelation
        fields = ('id', '_tag')


class SnippetSerializer(serializers.ModelSerializer):
    # use the custom serializer to build a tag list
    tags = TagSnippetRelationSerializer(many=True)

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'url', 'color', 'tags',
                  'pinned', 'starred', 'archived',
                  'created', 'modified')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('pk', 'first_name', 'last_name')


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password

    NOTE: This is an override for django-rest-auth's default
        UserDetailsSerializer class, in order to provide more
        details about the user.
    """
    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'date_joined', 'last_login')
        read_only_fields = ('email',)
