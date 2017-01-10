from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View

from rest_framework import generics, mixins, parsers, permissions, renderers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import UserDetailsSerializer


class UserExistsCheck(APIView):
    throttle_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        print(request.GET.get('username'))
        content = {}
        try:
            username = request.GET.get('username')
            User.objects.get(username=username)
            content = {'user': username}
        except User.DoesNotExist:
            pass
        return Response(content)


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

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        https://github.com/Tivix/django-rest-auth/issues/275
        """
        return get_user_model().objects.none()
