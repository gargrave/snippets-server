from django.conf.urls import include, url
from django.contrib import admin

from api_snippets_v1 import views, views_auth

admin.autodiscover()

urlpatterns = [
    # index view--basically just a blank page
    url(r'^$', views.index, name='index'),

    # admin view
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views_auth.ObtainAuthToken.as_view()),

    url(r'^api/v1/', include('api_snippets_v1.urls', namespace='api_v1')),
]
