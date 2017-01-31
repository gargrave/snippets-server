from django.contrib import admin

from .models import Snippet, Tag, TagSnippetRelation, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'owner')


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'url', 'color',
        'pinned', 'starred', 'archived',
        'created', 'modified')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title')


@admin.register(TagSnippetRelation)
class TagSnippetRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', '_tag', '_snippet')
