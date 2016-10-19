from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^snippets', views.SnippetList.as_view()),
]
