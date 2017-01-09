from django.conf.urls import include, url
from django.contrib import admin

from api_snippets_v1 import views, views_auth

admin.autodiscover()

urlpatterns = [
    # index view--basically just a blank page
    url(r'^$', views.index, name='index'),

    # admin view
    url(r'^admin/', include(admin.site.urls)),

    # django-rest-auth URLs
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'^api/v1/', include('api_snippets_v1.urls', namespace='api_v1')),
]
