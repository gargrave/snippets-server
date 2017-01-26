from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Snippet, UserProfile

# Get the UserModel
UserModel = get_user_model()


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'url', 'color',
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
