from django.conf.urls import url

from . import views, views_tags


urlpatterns = [
    url(r'^snippets/?$', views.SnippetList.as_view()),
    url(r'^snippets/archived/?$', views.ArchivedSnippetList.as_view()),
    url(r'^snippets/starred/?$', views.StarredSnippetList.as_view()),
    url(r'^snippets/search/?$', views.SnippetAdvancedSearch.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/?$', views.SnippetDetail.as_view()),

    url(r'^tags/?$', views_tags.TagList.as_view()),
    url(r'^tags/add/?$', views_tags.TagSnippetRelationCreateView.as_view()),
    url(r'^tags/remove/?$', views_tags.TagSnippetRelationDeleteView.as_view()),
    url(r'^tags/delete/(?P<pk>[0-9]+)/?$', views_tags.TagDeleteView.as_view()),
]
