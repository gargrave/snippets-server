from django.conf.urls import include, url
from django.contrib import admin

from api_snippets_v1 import views, views_auth, views_templates

admin.autodiscover()

urlpatterns = [
    url(r'^$', views_templates.Index.as_view(), name='index'),

    # admin view
    url(r'^admin/', include(admin.site.urls)),

    # URL for accessing a user's profile; note that this is NOT
    # actually a part of django-rest-auth, but we are using the same
    # URL base for simplicity's sake
    url(r'^rest-auth/user/profile/', views_auth.UserProfileDetailsView.as_view()),

    # django-rest-auth URLs
    # overriding /user/ to use our customized version
    url(r'^rest-auth/user/', views_auth.UserDetailsView.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/usercheck', views_auth.UserExistsCheck.as_view()),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # Snippets API
    url(r'^api/v1/', include('api_snippets_v1.urls', namespace='api_v1')),
]
