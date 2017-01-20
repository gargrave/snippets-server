from django.conf.urls import include, url
from django.contrib import admin

from api_snippets_v1 import views, views_auth, views_templates

admin.autodiscover()

urlpatterns = [
    url(r'^$', views_templates.Index.as_view(), name='index'),

    # admin view
    url(r'^admin/', include(admin.site.urls)),

    # django-rest-auth URLs
    # overriding /user/ to use our customized version
    url(r'^rest-auth/user/', views_auth.UserDetailsView.as_view()),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/usercheck', views_auth.UserExistsCheck.as_view()),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    url(r'^api/v1/', include('api_snippets_v1.urls', namespace='api_v1')),
]
