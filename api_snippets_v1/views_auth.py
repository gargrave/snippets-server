from django.contrib.auth.models import User

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserDetailsSerializer, UserProfileSerializer


class EmailExistsCheck(APIView):
    throttle_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        content = {}
        try:
            email = request.data.get('email')
            User.objects.get(email=email)
            content = {'email': email}
        except User.DoesNotExist:
            pass
        return Response(content)


class UserExistsCheck(APIView):
    throttle_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        content = {}
        try:
            username = request.data.get('username')
            User.objects.get(username=username)
            content = {'user': username}
        except User.DoesNotExist:
            pass
        return Response(content)


class UserProfileDetailsView(generics.RetrieveUpdateAPIView):
    """
    View for accessing a user's Profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.get_queryset()

    def get_queryset(self):
        user, created = UserProfile.objects.get_or_create(
            owner=self.request.user)
        return user


class UserDetailsView(generics.RetrieveUpdateAPIView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.
    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email
    Returns UserModel fields.

    NOTE: This is an override of django-rest-auth's default UserDetailsView
        in order to use our custom UserDetailsSerializer class for the serializer.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
