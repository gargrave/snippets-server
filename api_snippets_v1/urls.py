from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^snippets/?$', views.SnippetList.as_view()),
    url(r'^snippets/archived/?$', views.ArchivedSnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/?$', views.SnippetDetail.as_view()),
]
