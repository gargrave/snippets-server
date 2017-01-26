from django.contrib import admin

from .models import Snippet, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'owner')


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'url', 'color',
        'pinned', 'starred', 'archived',
        'created', 'modified')
